import _tkinter
import random
from tkinter import *
import time
import copy
import numpy as np
import pickle as pk
from sklearn.neural_network import MLPClassifier as MLP
import os
# Vars --------------------
eastWallPixels = []
westWallPixels = []
pixels = []
Train = True
Setup = True
gameSpeed = (100 - float(input(
    "Snake speed (set between 0 - 100%): "))) * .399 / 100 + .001  # .001 time delay for update the next frame (second)
pixelsLengthCount = int(input("Number of width pixels (defult: 20): "))  # Pixels count of plane length
spaceBetweenPixels = .90  # space between two pixels (percent)
DataCountForTrain = 10000
outlineColorOfPixels = "black"
planeColor = "black"
window_size = "800x610"  # size of window
programName = "Snake"
# ----------------------------


try:

    # Location Class
    class LOCATION:
        Loop = True
        snakeBudy = [0]
        targetLocation = 0
        nextMove = ""
        GAMECOLOR = "red"
        frame = 1
        previousFrame = 0
        score = 0
        wallsEnable = True
        startPermission = False
        isAIActivated = False


    # Define Functions

    # Wall Button
    def wall_Button():
        if LOCATION.wallsEnable:
            LOCATION.wallsEnable = False
            wallButton.config(text="Deactive", bg="white", fg="black")
        else:
            LOCATION.wallsEnable = True
            wallButton.config(text="Active", bg="black", fg="white")


    # AI Button
    def AI_Button():
        if LOCATION.isAIActivated:
            LOCATION.isAIActivated = False
            AIButton.config(text="Deactive", bg="white")
            LOCATION.snakeHeadColor = "yellow"
            show([LOCATION.snakeBudy[0]], "yellow")
            window.update_idletasks()
            window.update()

        else:
            LOCATION.isAIActivated = True
            AIButton.config(text="Active", bg="blue")
            LOCATION.snakeHeadColor = "blue"
            show([LOCATION.snakeBudy[0]], "blue")
            window.update_idletasks()
            window.update()


    # keybord Event handler
    def onKeyPress(event):
        key = event.keycode
        # if others keys pressed ignore
        if key in list(range(37, 41)):
            # if frame didn't update ignore
            if LOCATION.previousFrame < LOCATION.frame:
                # allow first frame to Start
                LOCATION.startPermission = True

                # handel inputs
                if key == 37:
                    # if key was the opposite of the next move do ignore
                    if LOCATION.nextMove == "r":
                        pass
                    else:
                        LOCATION.previousFrame = LOCATION.frame
                        LOCATION.nextMove = "l"

                elif key == 38:
                    # if key was the opposite of the next move do ignore
                    if LOCATION.nextMove == "d":
                        pass
                    else:
                        LOCATION.previousFrame = LOCATION.frame
                        LOCATION.nextMove = "u"

                elif key == 39:
                    # if key was the opposite of the next move do ignore
                    if LOCATION.nextMove == "l":
                        pass
                    else:
                        LOCATION.previousFrame = LOCATION.frame
                        LOCATION.nextMove = "r"

                elif key == 40:
                    # if key was the opposite of the next move do ignore
                    if LOCATION.nextMove == "u":
                        pass
                    else:
                        LOCATION.previousFrame = LOCATION.frame
                        LOCATION.nextMove = "d"
        else:
            pass


    # turn on the Locations
    def show(box, color="white"):
        for i in box:
            canvase.itemconfig(i, fill=color)


    # turn off the Locations
    def hide(box):
        for i in box:
            canvase.itemconfig(i, fill="black")


    # calculate next head location
    def nextHeadLocation(x):
        if LOCATION.nextMove == "l":
            LOCATION.snakeBudy.reverse()
            LOCATION.snakeBudy.append(x - 1)
            LOCATION.snakeBudy.reverse()
        elif LOCATION.nextMove == "u":
            LOCATION.snakeBudy.reverse()
            LOCATION.snakeBudy.append(x - pixelsLengthCount)
            LOCATION.snakeBudy.reverse()
        elif LOCATION.nextMove == "r":
            LOCATION.snakeBudy.reverse()
            LOCATION.snakeBudy.append(x + 1)
            LOCATION.snakeBudy.reverse()
        elif LOCATION.nextMove == "d":
            LOCATION.snakeBudy.reverse()
            LOCATION.snakeBudy.append(x + pixelsLengthCount)
            LOCATION.snakeBudy.reverse()


    # set a new target
    def newTarget():
        a = LOCATION.snakeBudy.copy()
        b = dict()
        a = list(b.fromkeys(a).keys())
        if a.__len__() < pixels_count:
            LOCATION.GAMECOLOR = "red"
            while True:
                LOCATION.targetLocation = random.randint(0, pixels_count)
                # if random location of target was on the snake's budy do it again
                if LOCATION.targetLocation in LOCATION.snakeBudy:
                    pass
                else:
                    break
        else:
            LOCATION.GAMECOLOR = "green"
            LOCATION.Loop = False


    def chekMove(AIPredict):
        targy = int(LOCATION.targetLocation / pixelsLengthCount)
        heady = int(LOCATION.snakeBudy[0] / pixelsLengthCount)
        targx = LOCATION.targetLocation % pixelsLengthCount
        headx = LOCATION.snakeBudy[0] % pixelsLengthCount
        if LOCATION.nextMove == "l" and AIPredict == "r":
            if heady < targy:
                AIPredict = "d"
            elif heady == targy:
                if heady == 0:
                    AIPredict = "d"
                else:
                    AIPredict = "u"
            else:
                AIPredict = "u"
        elif LOCATION.nextMove == "u" and AIPredict == "d":
            if headx < targx:
                AIPredict = "r"
            elif headx == targx:
                if LOCATION.snakeBudy[0] in westWallPixels:
                    AIPredict = "r"
                elif LOCATION.snakeBudy[0] in eastWallPixels:
                    AIPredict = "l"
                else:
                    AIPredict = "r"
            else:
                AIPredict = "l"
        elif LOCATION.nextMove == "r" and AIPredict == "l":
            if heady < targy:
                AIPredict = "d"
            elif heady == targy:
                if heady == 0:
                    AIPredict = "d"
                elif heady == pixelsLengthCount - 1:
                    AIPredict = "u"
                else:
                    AIPredict = "u"
            else:
                AIPredict = "u"
        elif LOCATION.nextMove == "d" and AIPredict == "u":
            if headx < targx:
                AIPredict = "r"
            elif headx == targx:
                if LOCATION.snakeBudy[0] in westWallPixels:
                    AIPredict = "r"
                elif LOCATION.snakeBudy[0] in eastWallPixels:
                    AIPredict = "l"
                else:
                    AIPredict = "r"
            else:
                AIPredict = "l"
        return AIPredict


    def AI():
        targy = int(LOCATION.targetLocation / pixelsLengthCount)
        heady = int(LOCATION.snakeBudy[0] / pixelsLengthCount)
        targx = LOCATION.targetLocation % pixelsLengthCount
        headx = LOCATION.snakeBudy[0] % pixelsLengthCount
        if Train:
            x1 = ((headx - targx) + (pixelsLengthCount - 1)) / ((pixelsLengthCount - 1) * 2)
            x2 = ((heady - targy) + 29) / 58
            AIpredict = int(mlp.predict(np.array([x1, x2]).reshape(1, -1)))
        else:
            AIpredict = int(mlp.predict(np.array([headx - targx, heady - targy]).reshape(1, -1)))
        if AIpredict == 1:
            out = "l"
        elif AIpredict == 2:
            out = "u"
        elif AIpredict == 3:
            out = "r"
        elif AIpredict == 4:
            out = "d"
        return out


    LOCATION.snakeHeadColor = "yellow"


    def Game():

        # calculate first location
        if pixelsLengthCount % 2 != 0:
            LOCATION.snakeBudy = [
                pixels[int(((pixelsLengthCount - 1) / 2) * pixelsLengthCount + (pixelsLengthCount - 1) / 2)]]
        else:
            LOCATION.snakeBudy = [pixels[int(((pixelsLengthCount - 1) / 2) * pixelsLengthCount)]]

        # set initial paramiters
        LOCATION.nextMove = ""
        LOCATION.previousFrame = 0
        LOCATION.frame = 1
        LOCATION.score = 0
        LOCATION.startPermission = False
        LOCATION.Loop = True
        lastLocations = [[]]

        # config GR elements
        frameTextbox.config(text="Frame : 0")
        scoreTextbox.config(text="Score : 0")
        gameoverTextbox.config(text="")
        restartButton.config(text="Restart")

        # pack elements
        frameTextbox.pack()
        scoreTextbox.pack()
        wallsTextbox.pack()
        AITextbox.pack()
        gameoverTextbox.pack()
        restartButton.pack()
        wallButton.pack()
        AIButton.pack()
        canvase.pack()

        # place elements
        canvase.place(x="3", y="2", anchor="nw")
        frameTextbox.place(x="690", y="20", anchor="ne")
        scoreTextbox.place(x="679", y="50", anchor="ne")
        wallsTextbox.place(x="666", y="427", anchor="ne")
        AITextbox.place(x="666", y="487", anchor="ne")
        gameoverTextbox.place(x="766", y="210", anchor="ne")
        restartButton.place(relx="0.93", rely="0.6", anchor="ne")
        wallButton.place(relx="0.93", rely="0.7", anchor="ne")
        AIButton.place(relx="0.93", rely="0.8", anchor="ne")
        wallsTextbox.config(text="Walls: ", font="bold 12")
        AITextbox.config(text="AI: ", font="bold 12")

        # Setup
        if Setup:
            newTarget()
            hide(list(range(1, pixels_count + 1)))
            show([LOCATION.targetLocation], "purple")
            show(LOCATION.snakeBudy, LOCATION.snakeHeadColor)

        # main Loop
        while LOCATION.Loop:
            if LOCATION.startPermission:
                if LOCATION.isAIActivated:
                    AIpredict = AI()
                    AIpredict = chekMove(AIpredict)
                    LOCATION.nextMove = AIpredict
                    print("Command:{0} , Target Location:{1} , Head Location:{2}".format(LOCATION.nextMove,
                                                                                 LOCATION.targetLocation,
                                                                                 LOCATION.snakeBudy[0]))
                # add last location to last list
                lastLocations.append(LOCATION.snakeBudy[:])

                # calculate next pixel that snake should go
                nextHeadLocation(LOCATION.snakeBudy[0])

                # hide the end of the tail
                hide([LOCATION.snakeBudy[-1]])

                # delete the end of the tail
                del LOCATION.snakeBudy[-1]

                # if snake got the target
                if LOCATION.targetLocation in LOCATION.snakeBudy:
                    # increase the score
                    LOCATION.score += 1

                    # if walls are Enabled
                    if LOCATION.wallsEnable:
                        # first we should now next location of the snake
                        nextHeadLocation(LOCATION.targetLocation)

                        # if snake hits the walls ---------------------------------

                        # North Wall
                        if LOCATION.snakeBudy[0] <= 0:
                            # show the last frame and end the game
                            show(lastLocations[1], "green")
                            show([LOCATION.targetLocation], "red")
                            LOCATION.Loop = False
                            break

                        # South Wall
                        elif LOCATION.snakeBudy[0] > pixels_count:
                            # show the last frame and end the game
                            show(lastLocations[1], "green")
                            show([LOCATION.targetLocation], "red")
                            LOCATION.Loop = False
                            break

                        # West Wall
                        elif LOCATION.snakeBudy[0] + 1 in westWallPixels and LOCATION.nextMove == "l":
                            # show the last frame and end the game
                            show(lastLocations[1], "green")
                            show([LOCATION.targetLocation], "red")
                            LOCATION.Loop = False
                            break

                        # East Wall
                        elif LOCATION.snakeBudy[0] - 1 in eastWallPixels and LOCATION.nextMove == "r":
                            # show the last frame and end the game
                            show(lastLocations[1], "green")
                            show([LOCATION.targetLocation], "red")
                            LOCATION.Loop = False
                            break

                        # --------------------------------------------------------

                    # if walls were disabled
                    else:

                        # North Wall
                        if LOCATION.snakeBudy[0] <= 0:
                            LOCATION.snakeBudy[0] += 1

                        # South Wall
                        elif LOCATION.snakeBudy[0] > pixels_count:
                            LOCATION.snakeBudy[0] -= 1

                        # East Wall
                        elif LOCATION.snakeBudy[0] - 1 in eastWallPixels and LOCATION.nextMove == "r":
                            LOCATION.snakeBudy[0] -= pixelsLengthCount - pixelsLengthCount

                        # West Wall
                        elif LOCATION.snakeBudy[0] + 1 in westWallPixels and LOCATION.nextMove == "l":
                            LOCATION.snakeBudy[0] += pixelsLengthCount + pixelsLengthCount

                        # else we should know next location of the snake
                        else:
                            nextHeadLocation(LOCATION.targetLocation)

                    # show the score
                    scoreTextbox.config(scoreTextbox, text="Score : " + str(LOCATION.score))

                    # set a New target and show the pixels
                    newTarget()
                    show(LOCATION.snakeBudy, "green")
                    show([LOCATION.targetLocation], "purple")

                # only just for make sure if Target was not set
                if LOCATION.targetLocation <= 0 or LOCATION.targetLocation > pixels_count:
                    newTarget()
                    show(LOCATION.snakeBudy, "green")
                    show([LOCATION.targetLocation], "purple")

                # walls crash event
                if LOCATION.wallsEnable:

                    # North Wall
                    if LOCATION.snakeBudy[0] <= 0:
                        # show the last frame and end the game
                        show(lastLocations[1], "green")
                        show([lastLocations[1][0]], "red")
                        gameoverTextbox.config(text="GAME OVER")
                        LOCATION.Loop = False
                        break

                    # South Wall
                    elif LOCATION.snakeBudy[0] > pixels_count:
                        # show the last frame and end the game
                        show(lastLocations[1], "green")
                        show([lastLocations[1][0]], "red")
                        gameoverTextbox.config(text="GAME OVER")
                        LOCATION.Loop = False
                        break

                    # East Wall
                    elif LOCATION.snakeBudy[0] - 1 in eastWallPixels and LOCATION.nextMove == "r":
                        # show the last frame and end the game
                        show(lastLocations[1], "green")
                        show([lastLocations[1][0]], "red")
                        gameoverTextbox.config(text="GAME OVER")
                        LOCATION.Loop = False
                        break

                    # West Wall
                    elif LOCATION.snakeBudy[0] + 1 in westWallPixels and LOCATION.nextMove == "l":
                        # show the last frame and end the game
                        show(lastLocations[1], "green")
                        show([lastLocations[1][0]], "red")
                        gameoverTextbox.config(text="GAME OVER")
                        LOCATION.Loop = False
                        break

                # if walls were disabled ( passing through the walls )
                else:

                    # Noth Wall
                    if LOCATION.snakeBudy[0] <= 0 and LOCATION.nextMove == "u":
                        LOCATION.snakeBudy[0] += pixels_count

                    # South Wall
                    elif LOCATION.snakeBudy[0] > pixels_count and LOCATION.nextMove == "d":
                        LOCATION.snakeBudy[0] -= pixels_count

                    # East Wall
                    elif LOCATION.snakeBudy[0] - 1 in eastWallPixels and LOCATION.nextMove == "r":
                        LOCATION.snakeBudy[0] -= pixelsLengthCount

                    # West Wall
                    elif LOCATION.snakeBudy[0] + 1 in westWallPixels and LOCATION.nextMove == "l":
                        LOCATION.snakeBudy[0] += pixelsLengthCount

                    # if target was there too
                    if LOCATION.targetLocation in LOCATION.snakeBudy:
                        # calculate next head location again
                        nextHeadLocation(LOCATION.targetLocation)

                        # ---
                        LOCATION.score += 1
                        scoreTextbox.config(scoreTextbox, text="Score : " + str(LOCATION.score))
                        newTarget()

                        # and show ---
                        show(LOCATION.snakeBudy, "green")
                        show([LOCATION.targetLocation], "purple")

                if not LOCATION.isAIActivated:
                    # self crash event
                    if LOCATION.snakeBudy[0] in LOCATION.snakeBudy[1:]:
                        # show the last frame and end the game
                        show(lastLocations[1], "green")
                        show([lastLocations[1][0]], "red")
                        gameoverTextbox.config(text="GAME OVER")
                        break
                else:
                    pass
                # reset all pixels
                hide(list(range(1, pixels_count + 1)))

                # show and go to the next frame
                show([LOCATION.targetLocation], "purple")
                show(LOCATION.snakeBudy[1:], "green")
                show([LOCATION.snakeBudy[0]], LOCATION.snakeHeadColor)

                # show number of the frame
                LOCATION.frame += 1
                frameTextbox.config(frameTextbox, text="Frame : " + str(LOCATION.frame))

                # delay untill the next frame
                time.sleep(gameSpeed)

                # delete secend past frame of the snake
                del lastLocations[0]

            # update the window
            window.update_idletasks()
            window.update()

        # show game over in the end
        gameoverTextbox.config(text="GAME OVER", fg=LOCATION.GAMECOLOR)


    # ---------------------------------------------------------------------------------------------------------------------

    # prepare values
    pixels_count = pixelsLengthCount ** 2
    width = int(window_size[0:3]) - 200
    height = int(window_size[4:]) - 10

    # build the window and set paramiters
    window = Tk()
    window.title(programName)
    window.config(bg=outlineColorOfPixels)
    window.geometry(window_size)
    window.resizable(False, False)

    # build plane and Buttons and Textboxes
    canvase = Canvas(window, width=width, height=height, bg=planeColor)
    restartButton = Button(window, width=9, height=1, text="Start", command=Game)
    wallButton = Button(window, width=9, height=1, text="Active", bg="black", fg="white", command=wall_Button)
    AIButton = Button(window, width=9, height=1, text="Deactive", command=AI_Button)
    frameTextbox = Label(window, bg="black", fg="white")
    scoreTextbox = Label(window, bg="black", fg="red")
    wallsTextbox = Label(window, bg="black", fg="white")
    AITextbox = Label(window, bg="black", fg="white")
    gameoverTextbox = Label(window, bg="black", fg="red", font="bold 15")

    # prepare values
    pixelsLength = (width * spaceBetweenPixels) / pixelsLengthCount
    spaceBetweenPixelsLength = (width - pixelsLength * pixelsLengthCount) / (pixelsLengthCount + 1)

    # set Keyboard event handler
    window.bind('<KeyPress>', onKeyPress)

    # build all pixels
    for i in range(pixelsLengthCount):
        for j in range(pixelsLengthCount):
            pixels.append(
                canvase.create_rectangle((j + 1) * spaceBetweenPixelsLength + pixelsLength * j,
                                         (i + 1) * spaceBetweenPixelsLength + pixelsLength * i,
                                         (j + 1) * spaceBetweenPixelsLength + pixelsLength * (j + 1),
                                         (i + 1) * spaceBetweenPixelsLength + pixelsLength * (i + 1),
                                         fill="black", outline=outlineColorOfPixels))

    # find the center of the board
    if pixelsLengthCount % 2 != 0:
        LOCATION.snakeBudy = [
            pixels[int(((pixelsLengthCount - 1) / 2) * pixelsLengthCount + (pixelsLengthCount - 1) / 2)]]
    else:
        LOCATION.snakeBudy = [pixels[int(((pixelsLengthCount - 1) / 2) * pixelsLengthCount)]]

    # find the walls
    for i in range(pixelsLengthCount):
        westWallPixels.append(pixels[i * pixelsLengthCount])
        eastWallPixels.append(pixels[pixelsLengthCount * (i + 1) - 1])

    # ---------------------------------------------------------------------------------------------------------------------
    # Neural Network vars & Functions ------------------------------------------------------------------------------
    if Train:
        Data = []

        # preparing DATA
        for i in range(int(DataCountForTrain / 2)):
            while True:
                targy = random.randint(1, pixelsLengthCount)
                heady = random.randint(1, pixelsLengthCount)
                targx = random.randint(1, pixelsLengthCount)
                headx = random.randint(1, pixelsLengthCount)
                if targy == heady and targx == headx:
                    pass
                else:
                    break

            if headx - targx < 0:
                Data.append([headx - targx, heady - targy, 3])
            elif headx - targx > 0:
                Data.append([headx - targx, heady - targy, 1])
        for i in range(int(DataCountForTrain / 2)):
            while True:
                targy = random.randint(1, pixelsLengthCount)
                heady = random.randint(1, pixelsLengthCount)
                if targy == heady and targx == headx:
                    pass
                else:
                    break

            if heady - targy < 0:
                Data.append([0, heady - targy, 4])
            elif heady - targy > 0:
                Data.append([0, heady - targy, 2])

        # normalizing train DATA
        normalizData = copy.copy(Data)
        min = np.min(Data)
        max = np.max(Data)
        for i in range(len(Data)):
            for j in range(2):
                normalizData[i][j] = (Data[i][j] - min) / (max - min)

        # separation DATA
        y = []
        x = []
        for i in normalizData:
            y.append(i[-1])
            x.append([i[0], i[1]])

        # create and train neural network
        mlp = MLP(hidden_layer_sizes=(4, 3), activation="tanh", solver="sgd",
                  learning_rate="adaptive", max_iter=500, shuffle=True, tol=1e-5,
                  verbose=True, n_iter_no_change=10)

        mlp.fit(x, y)
    else:
        mlp = pk.load(open("AIsnake.sav", "rb"))
    # ------------------------------------------------------------------------------
    # start game
    Game()

    # hold the window
    while True:
        window.mainloop()
        window.destroy()
    # if window destroyed
except _tkinter.TclError:
    pass

os.system("cls")
print("-----------------------------------\n\n")
print("Developed by : Ali Bagheri")
print("Email : Ali.bagheri98@gmail.com\n\n")
print("-----------------------------------")
time.sleep(3)
