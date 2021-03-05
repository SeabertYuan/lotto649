import pygame
import pygame_gui
import lotto649driver as ld

#0 Start by asking whether or not they want to generate their numbers
#1 If yes, move to step 3
#2 If no, ask them 6 times for a number
#3 Confirm their numbers, if yes, say locked in and move to step 5
#4 Change numbers based on which index they give.
#5 Generate 6 random numbers as the winning ticket
#5 One by one show them and way whether or not they won
#5 Show odds of winning for every win
#6 Ask if they want to play again and either do nothing (no) or restart (yes)

pygame.init() #Initialize pygame
pygame.mixer.init()
backend = ld.lottologic() # make a new object

pygame.display.set_caption('Lotto 649') #Set title of window to 'Lotto 649'
window_surface = pygame.display.set_mode((800, 600)) #Set window to 800px by 600px (x,y)

#Sets the background to the window size and sets the colour to black
background = pygame.Surface((800, 600))
background.fill(pygame.Color('#FF6EC7'))

manager = pygame_gui.UIManager((800, 600)) #manages every element on the window
pygame.mixer.music.load('song2.wav') #sets the background music to song2.wav, change this to whatever song you'd like
pygame.mixer.music.play() #plays the song

text = '<b>Welcome to lotto 649!<br>Would you like to generate random numbers? (Yes/No)</b>' #initialize initial text
selected_number = '<b></b>' #initialize empty ticket

#Box that contains text to be displayed
information_box = pygame_gui.elements.UITextBox(text,
                                                    relative_rect=pygame.Rect((250,50),(300,150)),
                                                    manager=manager)
information_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
#Box that displays your ticket number
number_box = pygame_gui.elements.UITextBox(selected_number,
                                           relative_rect=pygame.Rect((275,200),(250,50)),
                                           manager=manager)
#Button that is for yes
yes_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 375), (100, 50)), text='Yes',
                                                    manager=manager)
#Button that is for no
no_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((425, 375), (100, 50)),
                                         text='No',
                                         manager=manager)
#Button at the very end to prompt the user for results
result_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 325), (150,35)),
                                             text='Press for result',
                                             manager=manager)
result_button.hide() #hide the button by default

### Updates a boxes text
def change_information(text, information_box):
#Updates the box
    information_box = pygame_gui.elements.UITextBox(text,
                                                    relative_rect=pygame.Rect((250,50),(300,150)),
                                                    manager=manager)
    information_box.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)
#Field for entering number
number_entry = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((350, 275), (100,150)),
                                                   manager=manager)
def change_number_display(selected_number, number_box):
#Box that displays your ticket number
    number_box = pygame_gui.elements.UITextBox(selected_number,
                                               relative_rect=pygame.Rect((275,200),(250,50)),
                                               manager=manager)

clock = pygame.time.Clock() #used by pygame_gui to look for input updates
is_running = True
stage = 0 # stages 0-6 0 is start stage, all the way to reset stage (see above)
i = 1 #variable for looking through ticket_numbers, and for changing ticket_numbers

#function to call and change the textbox used in stage 5
def compare(text, information_box):
    text = backend.winningNums(text)
    change_information(text, information_box)

#While pygame is running
while is_running:
    time_delta = clock.tick(60)/1000.0
    number_entry.set_allowed_characters('numbers')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        manager.process_events(event)
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == yes_button:
                    print('Yes button pressed.')
                    if stage == 0: #if yes pressed when asked to generate numbers
                        backend.yn_button = 1
                        backend.generated_num()
                        stage=2
                        text = backend.confirm_numbers(text)
                        change_information(text, information_box)
                        for num in backend.ticket_numbers:
                            if selected_number.endswith('</b>'):
                                selected_number = selected_number[:-4]+str(num)+' </b>'
                        change_number_display(selected_number, number_box)
                        backend.yn_button = 0
                    elif stage == 2: #if yes pressed when asked to confirm
                        stage = 5
                        backend.yn_button = 1
                        text = backend.change_numbers(text, backend.yn_button)
                        change_information(text, information_box)
                        no_button.disable()
                        yes_button.disable()
                        backend.yn_button = 0
                        compare(text, information_box)
                        result_button.show()
                    elif stage == 6: #when yes pressed when asked to reset
                        stage = 0
                        i = 1
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load('song2.wav')
                        pygame.mixer.music.play()
                        selected_number = '<b></b>'
                        change_number_display(selected_number, number_box)
                        text = '<b>Welcome to lotto 649!<br>Would you like to generate random numbers? (Yes/No)</b>'
                        change_information(text, information_box)
                        backend = ld.lottologic()
                        
                if event.ui_element == no_button:
                    print('No button pressed.')
                    if stage == 0: #if no pressed when asked to generate numbers
                        backend.yn_button = 2
                        stage=1
                        change_information(backend.choose_number(text), information_box)
                    elif stage == 2: #if no pressed when asked to confirm
                        stage = 3
                        backend.yn_button = 2
                        change_information(backend.change_numbers(text, backend.yn_button), information_box)

                if event.ui_element == result_button:
                    print('Result button pressed.')
                    if stage == 5: #when the result button is pressed when numbers are locked in
                        pygame.mixer.music.unload() #reset all previous songs
                        pygame.mixer.music.load('song.wav') #switch the song to song1.wav
                        pygame.mixer.music.play() #play song1.wav
                        text = backend.comparison(text)[:-4]+'<br>Retry? (Yes/No)</b>'
                        change_information(text, information_box)
                        result_button.hide() #hide result button
                        yes_button.enable() #re-enable the yes button
                        no_button.enable() #re-enable the no button
                        stage = 6
            if event.user_type == pygame_gui.UI_TEXT_ENTRY_CHANGED:
                if event.ui_element == number_entry:
                    if stage == 1 and backend.yn_button == 2: #if selecting numbers and no was pressed
                        write_string = str(event.text)
                        if selected_number.endswith('</b>'):
                            selected_number = selected_number[:-4] + write_string
                        selected_number += '</b>'
                        write_string = ''
                        change_number_display(selected_number, number_box)
                        selected_number = '<b></b>'
                        for number in backend.ticket_numbers:
                            selected_number = selected_number[:-4]+str(number)+' </b>'

            if event.user_type  == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                if len(str(event.text)) <= 0: #checks for empty boxes
                    text = '<b>Enter a valid number!</b>'
                    change_information(text, information_box)
                else:
                    if stage == 1: #when asked to choose numbers
                        if i < 7: #will do while i is between 1 and 6 inclusive
                            promise = backend.choose_one_number(backend.ticket_numbers, event.text)
                            if promise in range(1,50): #Check if number is within range 1-49
                                backend.ticket_numbers.append(int(promise)) #add number to ticket_numbers
                                if selected_number.endswith('</b>'):
                                    selected_number = selected_number[:-4]+str(promise)+' '
                            else:
                                text = promise
                                change_information(text, information_box)
                                i-=1
                            i+=1
                        if i > 6:
                            stage=2
                            text = backend.confirm_numbers(text)
                            change_information(text, information_box)
                        change_number_display(selected_number, number_box)
                        number_entry.set_text('')
                    elif stage == 3: #called when no is pressed when asked to confirm numbers
                        i = int(event.text)
                        text = backend.select_change(event.text, text)
                        change_information(text, information_box)
                        number_entry.set_text('')
                        stage = 4
                    elif stage == 4: #when changing number
                        promise = backend.choose_one_number(backend.ticket_numbers, event.text)
                        if promise in range(1,50):
                            backend.ticket_numbers[i-1] = promise
                        number_entry.set_text('')
                        selected_number = '<b>'
                        for num in backend.ticket_numbers:
                            selected_number += str(num)+' '
                        selected_number += '</b>'
                        change_number_display(selected_number, number_box) #Updates ticket display
                        text = backend.confirm_numbers(text)
                        change_information(text, information_box)
                        stage = 2

    manager.update(time_delta)
    information_box.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
