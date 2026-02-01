import uuid
from abc import ABC,abstractmethod
from datetime import datetime
from enum import Enum

class User:
    def __init__(self,name):
        self.id=str(uuid.uuid4())
        self.name=name
        self.reputation=0

    def update_reputation(self,points):
        self.reputation += points

    def get_ID(self):
        return self.id

    def get_Name(self):
        return self.name
    
    def get_Reputation(self):
        return self.reputation

    
class Content(ABC):
    def __init__(self,content_id,body,author):
        self.id=content_id
        self.body=body
        self.author=author
        self.creation_date=datetime.now()

    def get_ID(self):
        return self.id
    
    def get_Body(self):
        return self.body

    def get_Author(self):
        return self.author

class VoteType(Enum):
    UPVOTE="UPVOTE"
    DOWNVOTE="DOWNVOTE"

class EventType(Enum):
    UPVOTE_QUESTION="UPVOTE_QUESTION"
    DOWNVOTE_QUESTION="DOWNVOTE_QUESTION"
    UPVOTE_ANSWER="UPVOTE_ANSWER"
    DOWNVOTE_ANSWER="DOWNVOTE_ANSWER"
    ACCEPT_ANSWER="ACCEPT_ANSWER"
    
class Post(Content):
    def __init__(self,post_id,body,author):
        super().__init__(post_id,body,author)
        self.votes=0
        self.voters={}
        self.comments=[]
        self.observers=[]
    
    def addObserver(self,observer):
        self.observers.append(observer)
    
    def notifyObservers(self,event):
        for observer in self.observers:
            observer.on_post_event(event)
    
    def vote(self,user,voteType):
        user_id=user.get_ID()
        if user_id in self.voters and self.voters[user_id]==voteType:
            return "User has already voted"
        score=0
        if user_id in self.voters:
            score=2 if voteType==VoteType.UPVOTE else -2
        else:
            score=1 if voteType==VoteType.UPVOTE else -1
        self.votes += score
        self.voters[user_id]=voteType

        if isinstance(self,Question):
            event_type=EventType.UPVOTE_QUESTION if voteType==VoteType.UPVOTE else EventType.DOWNVOTE_QUESTION
        else:
            event_type=EventType.UPVOTE_ANSWER if voteType==VoteType.UPVOTE else EventType.DOWNVOTE_ANSWER
        self.notifyObservers(Event(event_type,user,self))
        return "Vote recorded"

class Tag:
    def __init__(self,name):
        self.name=name
    def get_Name(self):
        return self.name

class Question(Post):
    def __init__(self,title,body,author,tags):
        super().__init__(str(uuid.uuid4()),body,author)
        self.title=title
        self.tags=tags
        self.answers=[]
        self.author=author
        self.accepted_answer=None

    def add_Answer(self,answer):
        self.answers.append(answer)
    
    def accept_Answer(self,answer):
        if not self.author.get_ID()==answer.get_Author().get_ID():
            self.accepted_answer=answer
            answer.set_Accepted(True)
            self.notifyObservers(Event(EventType.ACCEPT_ANSWER,answer.get_Author(),answer))

    def get_title(self):
        return self.title

    def get_tags(self):
        return self.tags
    
    def get_answers(self):
        return self.answers
    
    def get_Author(self):
        return self.author

class Answer(Post):
    def __init__(self,body,author):
        super().__init__(str(uuid.uuid4()),body,author)
        self.is_accepted=False

    def set_Accepted(self,accepted):
        self.is_accepted=accepted

    def get_IsAccepted(self):
        return self.is_accepted

class Comment(Content):
    def __init__(self,body,author):
        super().__init__(str(uuid.uuid4()),body,author)
    
class Event:
    def __init__(self,event_type,user,target=None):
        self.event_type=event_type
        self.user=user
        self.target=target
        self.timestamp=datetime.now()

    def get_type(self):
        return self.event_type
    
    def get_user(self):
        return self.user

    def get_target(self):
        return self.target

class PostObserver(ABC):
    @abstractmethod
    def on_post_event(self,event):
        pass

class ReputationManager(PostObserver):
    QUESTION_UPVOTE_POINTS=5
    QUESTION_DOWNVOTE_POINTS=-2
    ANSWER_UPVOTE_POINTS=10
    ANSWER_DOWNVOTE_POINTS=-2
    ACCEPT_ANSWER_POINTS=15
    def on_post_event(self,event):
        post_author=event.get_target().get_Author()
        if event.get_type()==EventType.UPVOTE_QUESTION:
            post_author.update_reputation(self.QUESTION_UPVOTE_POINTS)
        elif event.get_type()==EventType.DOWNVOTE_QUESTION:
            post_author.update_reputation(self.QUESTION_DOWNVOTE_POINTS)
        elif event.get_type()==EventType.UPVOTE_ANSWER:
            post_author.update_reputation(self.ANSWER_UPVOTE_POINTS)
        elif event.get_type()==EventType.DOWNVOTE_ANSWER:
            post_author.update_reputation(self.ANSWER_DOWNVOTE_POINTS)
        elif event.get_type()==EventType.ACCEPT_ANSWER:
            post_author.update_reputation(self.ACCEPT_ANSWER_POINTS)

class SearchStrategy(ABC):
    @abstractmethod
    def filter(self,questions):
        pass

class KeyWordSearchStrategy(SearchStrategy):
    def __init__(self,key):
        self.key=key.lower()

    def filter(self,questions):
        result=[]
        for question in questions:
            if self.key in question.get_title().lower() or self.key in question.get_Body().lower():
                result.append(question)
        return result

class TagSearchStrategy(SearchStrategy):
    def __init__(self,tag):
        self.tag=tag.lower()
    def filter(self,questions):
        result=[]
        for question in questions:
            for t in question.get_tags():
                if t.get_Name().lower()==self.tag:
                    result.append(question)
                    break
        return result

class UserSearchStrategy(SearchStrategy):
    def __init__(self,user):
        self.user=user
    def filter(self,questions):
        result=[]
        for question in questions:
            if question.get_Author().get_ID()==self.user.get_ID():
                result.append(question)
        return result

#facade
class StackOverflowService:
    def __init__(self):
        self.users={}
        self.questions={}
        self.answers={}
        self.reputation_manager=ReputationManager()

    def create_User(self,name):
        user=User(name)
        self.users[user.get_ID()]=user
        return user

    def post_Question(self,uid,title,body,author,tags):
        author=self.users[uid]
        question=Question(title,body,author,tags)
        question.addObserver(self.reputation_manager)
        self.questions[question.get_ID()]=question
        return question

    def post_Answer(self,uid,question_id,body):
        author=self.users[uid]
        question=self.questions[question_id]
        answer=Answer(body,author)
        answer.addObserver(self.reputation_manager)
        question.add_Answer(answer)
        self.answers[answer.get_ID()]=answer
        return answer

    def vote_Post(self,uid,post_id,voteType):
        user=self.users[uid]
        post=self.find_Post(post_id)
        return post.vote(user,voteType)

    def accept_Answer(self,question_id,answer_id):
        question=self.questions[question_id]
        answer=self.answers[answer_id]
        question.accept_Answer(answer)

    def search_questions(self,strategy):
        return strategy.filter(self.questions.values())

    def get_user(self,uid):
        return self.users[uid]

    def find_Post(self,post_id):
        if post_id in self.questions:
            return self.questions[post_id]
        elif post_id in self.answers:
            return self.answers[post_id]
        else:
            return None

class StackOverflowDemo:
    @staticmethod
    def main():
        service=StackOverflowService()
        
        user1=service.create_User("Alice")
        user2=service.create_User("Bob")
        user3=service.create_User("Charlie")

        print("Alice posts a question\n")

        python_tag=Tag("Python")
        design_tag=Tag("Design")
        tags=[python_tag,design_tag]
        question=service.post_Question(user1.get_ID(),"How to implement Observer pattern in Python?","I want to understand how to implement the Observer pattern in Python. Can someone provide an example?",user1,tags)
        
        print("Bob answers and charlie the question\n")
        answer1=service.post_Answer(user2.get_ID(),question.get_ID(),"You can use abstract base classes to define the Observer interface.")
        answer2=service.post_Answer(user3.get_ID(),question.get_ID(),"Consider using built-in libraries like 'observer' for easier implementation.")
        StackOverflowDemo.print_reputations(service)

        print("Voting on posts\n")
        service.vote_Post(user3.get_ID(),question.get_ID(),VoteType.UPVOTE)
        service.vote_Post(user1.get_ID(),answer1.get_ID(),VoteType.UPVOTE)
        service.vote_Post(user1.get_ID(),answer2.get_ID(),VoteType.UPVOTE)
        service.vote_Post(user2.get_ID(),answer2.get_ID(),VoteType.UPVOTE)
        StackOverflowDemo.print_reputations(service)
        print("Alice accepts Bob's answer\n")
        service.accept_Answer(question.get_ID(),answer1.get_ID())

        print("searching for questions with keyword 'python'\n")
        strategy=TagSearchStrategy("python")
        results=service.search_questions(strategy)
        for q in results:
            print(q.get_title())

        StackOverflowDemo.print_reputations(service)
        
    @staticmethod
    def print_reputations(service):
        print("User Reputations:")
        for user in service.users.values():
            print(f"{user.get_Name()}: {user.get_Reputation()}")

if __name__=="__main__":
    StackOverflowDemo.main()