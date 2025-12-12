from enums.playStrategyType import PlayStrategyType
from enums.deviceType import DeviceType
from musicPlayerApplication import MusicPlayerApplication


def main():
    try:
        application=MusicPlayerApplication.getInstance()

        application.createSongInLibrary("Kesariya", "Arijit Singh", "/music/kesariya.mp3")
        application.createSongInLibrary("Chaiyya Chaiyya", "Sukhwinder Singh", "/music/chaiyya_chaiyya.mp3")
        application.createSongInLibrary("Tum Hi Ho", "Arijit Singh", "/music/tum_hi_ho.mp3")
        application.createSongInLibrary("Jai Ho", "A. R. Rahman", "/music/jai_ho.mp3")
        application.createSongInLibrary("Zinda", "Siddharth Mahadevan", "/music/zinda.mp3")

        application.createPlayList("Bollywood Vibes")
        application.addSongToPlaylist("Bollywood Vibes", "Kesariya")
        application.addSongToPlaylist("Bollywood Vibes", "Chaiyya Chaiyya")
        application.addSongToPlaylist("Bollywood Vibes", "Tum Hi Ho")
        application.addSongToPlaylist("Bollywood Vibes", "Jai Ho")

        application.connectAudioDevice(DeviceType.BLUETOOTH)

        application.playSingleSong("Zinda")
        application.pauseCurrentSong("Zinda")
        application.playSingleSong("Zinda")

        print("\n-- Sequential Playback --\n")
        application.selectPlayStrategy(PlayStrategyType.SEQUENTIAL)
        application.loadPlaylist("Bollywood Vibes")
        application.playAllTracksInPlaylist()

        print("\n-- Random Playback --\n")
        application.selectPlayStrategy(PlayStrategyType.RANDOM)
        application.loadPlaylist("Bollywood Vibes")
        application.playAllTracksInPlaylist()

        print("\n-- Custom Queue Playback --\n")
        application.selectPlayStrategy(PlayStrategyType.CUSTOM_QUEUE)
        application.loadPlaylist("Bollywood Vibes")
        application.queueSongNext("Kesariya")
        application.queueSongNext("Tum Hi Ho")
        application.playAllTracksInPlaylist()

        print("\n-- Play Previous in Sequential --\n")
        application.selectPlayStrategy(PlayStrategyType.SEQUENTIAL)
        application.loadPlaylist("Bollywood Vibes")
        application.playAllTracksInPlaylist()

        application.playPreviousTrackInPlaylist()
        application.playPreviousTrackInPlaylist()
    
    except Exception as error:
        print("Error:", error)

if __name__ == "__main__":
    main()