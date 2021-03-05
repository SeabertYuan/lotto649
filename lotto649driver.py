import random
import math

### class that contains all functions and methods to run lottery
class lottologic:
    #initializes constructors
    def __init__(self):
        self.ticket_numbers = [] #chosen or generated numbers
        self.winning_numbers = [] #list for correct number set
        self.yn_button = 0 #0 for null, 1 for yes, 2 for no
    
### confirm the numbers on the ticket
    def confirm_numbers(self, text):
      text = '<b>Your numbers are:<br></b>'
      for num in self.ticket_numbers:
        if text.endswith('</b>'):
            text = text[:-4]
        text += str(num) + ' '
      text += '<br>Confirm? (Yes/No)</b>'
      return text

  ### determines whether or not a change needs to be done
    def change_numbers(self,text, yn_button):
        text = '<b></b>'
        if yn_button == 2:
            if text.endswith('</b>'):
                text = text[:-4]
            text += '<br>Which number would you like to change? (1-6)</b>'
            return text
        elif yn_button == 1:
            text = '<b>Numbers locked in!</b>'
            return text
        return text

    ### Takes user input to determine which number to change
    def select_change(self, number, text): #number is the user input
        if int(number) > 6 or int(number) < 1:
            text = '<b>Number out of range, keep number in range (1-6).</b>'
            return text
        text = '<b>Enter a number between 1 and 49, then press enter.</b>'
        return text

### gets one valid input at a time
    def choose_one_number(self, ticket_numbers, input_number):
        if int(input_number) > 49:
            text = '<b>Number is too large!</b>'
            return text
        if int(input_number) in ticket_numbers:
            text = '<b>Number already in list</b>'
            return text
        return int(input_number)

### user choosing numbers
    def choose_number(self, text):
        text = '<b>Enter a number in the text box between 1 and 49, and press enter.</b>' #sets text on information box
        return text

###  random generated numbers
    def generated_num(self):
      for i in range(1, 7):
        random_num = random.randint(1, 49)
        while random_num in self.ticket_numbers: #will keep generating random numbers until number is distinct
          random_num = random.randint(1, 49)
        self.ticket_numbers.append(random_num)

### Selects 6 random distinct numbers as the winning lottery numbers
    def winningNums(self, text):
        for i in range(6):
            newNum = random.randint(1,49)
            while newNum in self.winning_numbers:
                newNum = random.randint(1,49)
            self.winning_numbers.append(newNum)
        if text.endswith('</b>'):
            text = text[:-4]+'<br>Drawing numbers...'+'</b>'
        return text

    ### Compares the winning tickets to your ticket
    def comparison(self, text):
        sameCounter = 0
        text = '<b>Winning numbers are:<br></b>'
        for j in self.winning_numbers:
            if text.endswith('</b>'):
                text = text[:-4]+str(j)+' </b>'
        text = text[:-4]+'<br></b>'
        for i in self.ticket_numbers:
            if i in self.winning_numbers:
                if text.endswith('</b>'):
                    text = text[:-4]+'You won with: '+str(i)+'<br></b>'
                print("You won with: " + str(i))
                sameCounter+=1
        if sameCounter == 0:
            text = text[:-4]+"You didn't win!</b>"
        text = text[:-4]+'<br>Probability of: 1 in '+self.probability(sameCounter)+'</b>'
        return text

    ### Calculates probability
    def probability(self, numberWon): #calculates the probability of your winnings
        best_case = math.comb(49,6)
        if numberWon == 6:
            return str(best_case)
        else:
            winning_ticket = math.comb(6,numberWon)
            non_winning = math.comb(43,(6-numberWon))
            odds = round(100/((winning_ticket*non_winning)/best_case*100), 5)
            return str(odds)
