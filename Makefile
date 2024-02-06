all: RaceHorses


RaceHorses: 
	python.exe main.py video/RaceHorses_416x240_30.yuv 416 240 30 > bitstream.txt

BasketballDrive: 
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/1080p/BasketballDrive_1920x1080_50.yuv 1920 1080 3 > BasketballDrive_3Frames.txt

os1080:
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/1080p/ArenaOfValor_1920x1080_60_8bit_420.yuv 1920 1080 60 > ArenaOfValor_60frames.txt
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/1080p/MarketPlace_1920x1080_60fps_10bit_420.yuv 1920 1080 60 > MarketPlace_60frames.txt
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/1080p/RitualDance_1920x1080_60fps_10bit_420.yuv 1920 1080 60 > RitualDance_60frames.txt
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/1080p/BQTerrace_1920x1080_60.yuv 1920 1080 60 > BQTerrace_60frames.txt
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/1080p/Cactus_1920x1080_50.yuv 1920 1080 50 > Cactus_50frames.txt

ClasseE:
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/720p/FourPeople_1280x720_60.yuv 1280 720 60 > p720p_FourPeople_60frames.txt
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/720p/Johnny_1280x720_60.yuv 1280 720 60 > p720p_Johnny_60frames.txt
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/720p/KristenAndSara_1280x720_60.yuv 1280 720 60 > p720p_KristenAndSara_60frames.txt

ClasseCa:
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/480p/BQMall_832x480_60.yuv 832 480 60 > p480p_BQMall_60frames.txt
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/480p/PartyScene_832x480_50.yuv 832 480 50 > p480p_PartyScene_50frames.txt

ClasseC:
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/480p/RaceHorses_832x480_30.yuv 832 480 30 > p480p_RaceHorses480_30frames.txt
	python.exe main.py D:/Documents/referenceSoftwares/sequencias/480p/BasketballDrill_832x480_50.yuv 832 480 50 > p480p_BasketballDrill_50frames.txt
				