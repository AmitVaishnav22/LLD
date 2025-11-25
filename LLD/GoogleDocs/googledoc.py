from abc import ABC, abstractmethod


# Document Element Interface
class DocumentElement(ABC):
    @abstractmethod
    def render(self)-> str:
        pass

# concrete Document Elements
class TextElement(DocumentElement):
    def __init__(self,text:str):
        self.text = text
    def render(self)-> str:
        return self.text

class ImageElement(DocumentElement):
    def __init__(self,url:str):
        self.url = url
    def render(self)-> str:
        return f"<img src='{self.url}' />"

class TableElement(DocumentElement):
    def __init__(self,data:list):
        self.data = data
    def render(self)-> str:
        table_html = "<table>"
        for row in self.data:
            table_html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
        table_html += "</table>"
        return table_html

class NewLimeElement(DocumentElement):
    def render(self) -> str:
        return "\n"


# Document Class - Document HAS A collection of Document Elements
class Document:
    def __init__(self):
        self.elements=[]
    def add_element(self,element:DocumentElement):
        self.elements.append(element)
    def render(self)-> str:
        return "".join(e.render() for e in self.elements)

# Persistence Interface
class Persistence(ABC):
    @abstractmethod
    def save(self,data:str):
        pass

# Concrete Persistence Implementation for Google Docs
class FileStorage(Persistence):
    def __init__(self,filename="document.txt"):
        self.filename = filename
    def save(self,data:str):
        try:
            with open(self.filename,"w") as f:
                f.write(data)
            print(f"Document saved to {self.filename}")
        except Exception as e:
            print(f"Failed to save document: {e}")

class DBStorage(Persistence):
    def save(self,data:str):
        # Simulate saving to a database
        print("Document saved to the database.")
    
# Document Editor Class - CLient that uses Document and Persistence
class DocumentEditor:
    def __init__(self,document:Document,persistence:Persistence):
        self.document = document
        self.persistence = persistence
    def add_text(self,text:str):
        self.document.add_element(TextElement(text))
    def add_image(self,url:str):
        self.document.add_element(ImageElement(url))
    def add_table(self,data:list):
        self.document.add_element(TableElement(data))
    def add_newline(self):
        self.document.add_element(NewLimeElement())
    def render(self)-> str:
        return self.document.render()
    def save(self):
        data = self.render()
        self.persistence.save(data)

# Example Usage
if __name__ == "__main__":
    doc = Document()
    persistence = FileStorage()
    editor = DocumentEditor(doc,persistence)

    editor.add_text("Hello, this is a sample Google Doc.\n")
    editor.add_image("http://example.com/image.png")
    editor.add_newline()
    editor.add_table([["Name","Age"],["Alice",30],["Bob",25]])
    editor.add_newline()
    editor.add_text("End of the document.")
    print(editor.render())
    editor.save()


# This code defines a simple document editor system that allows adding text, images, tables, and new lines to a document.
# The document can be rendered as a string and saved using different persistence strategies (file or database).
