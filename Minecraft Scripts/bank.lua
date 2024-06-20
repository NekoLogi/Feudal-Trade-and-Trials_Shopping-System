local basalt = require("basalt") -- we need basalt here
local utils = require("bank_utils")

local main = basalt.createFrame():setTheme({FrameBG = colors.lightGray, FrameFG = colors.black}) -- we change the default bg and fg color for frames

local sub = { -- here we create a table where we gonna add some frames
    main:addFrame():setPosition(1, 2):setSize("parent.w", "parent.h - 1"), -- obviously the first one should be shown on program start
    main:addFrame():setPosition(1, 2):setSize("parent.w", "parent.h - 1"):hide(),
    main:addFrame():setPosition(1, 2):setSize("parent.w", "parent.h - 1"):hide(),
}

local function openSubFrame(id) -- we create a function which switches the frame for us
    if(sub[id]~=nil)then
        for k,v in pairs(sub)do
            v:hide()
        end
        sub[id]:show()
    end
end

local menubar = main:addMenubar():setScrollable() -- we create a menubar in our main frame.
    :setSize("parent.w")
    :onChange(function(self, val)
        openSubFrame(self:getItemIndex()) -- here we open the sub frame based on the table index
    end)
    :addItem("Willkommen")
    :addItem("Account")
    :addItem("Karte")

-- Now we can change our sub frames, if you want to access a sub frame just use sub[subid], some examples:
sub[1]:addLabel()
    :setText("Willkommen")
    :setPosition(21,2)
sub[1]:addLabel()
    :setText("MineTaler Bank!")
    :setPosition(19,4)
sub[1]:addLabel()
    :setText("Navigieren können Sie mit den Tabs oben angezeigt.")
    :setPosition(2,8)
sub[1]:addLabel()
    :setText("[Account]: Hier können Sie ein Konto erstellen")
    :setPosition(1,10)
sub[1]:addLabel()
    :setText("und Kontodaten verwalten.")
    :setPosition(12,11)
sub[1]:addLabel()
    :setText("[Karte]: Hier können Sie eine verlorene Karte")
    :setPosition(1,12)
sub[1]:addLabel()
    :setText("erstellen, sofern Sie die Daten kennen.")
    :setPosition(10,13)

sub[2]:addLabel()
    :setText("Wähle eine Option:")
    :setPosition(17,3)
sub[2]:addButton()
    :setText("Erstellen")
    :setPosition(20,5)
    :onClick(
        function()
            local createFrame = main:addFrame():setPosition(1, 2):setSize("parent.w", "parent.h - 1")
            createFrame:addLabel()
                :setText("Kartenname eingeben:")
                :setPosition(16,3)
            local accountUserField = createFrame:addInput()
                :setInputType("text")
                :setDefaultText("       Gustaf")
                :setInputLimit(20)
                :setSize(20,1)
                :setPosition(16,4)
            createFrame:addLabel()
                :setText("Pin eingeben:")
                :setPosition(16,8)
            local accountPinField = createFrame:addInput()
                :setInputType("password")
                :setInputLimit(4)
                :setSize(5,1)
                :setPosition(31,8)
            createFrame:addButton()
                :setText("Erstellen")
                :setPosition(20,14)
                :onClick(
                    function()
                        basalt.debug(utils.createAccount(accountUserField.getValue(), accountPinField.getValue()))
                        --local message = utils.createCard(cardUserField.getValue(), cardPinField.getValue())
                        --cardResultMessage.setText(message)
                        os.sleep(2)
                        os.reboot()
                    end)
        end)
sub[2]:addButton()
    :setText("Kontostand")
    :setPosition(20,9)
    :onClick(
        function()
            basalt.debug(utils.getAccount())
            --local message = utils.createCard(cardUserField.getValue(), cardPinField.getValue())
            --cardResultMessage.setText(message)
        end)

sub[3]:addLabel()
    :setText("Kartenname eingeben:")
    :setPosition(16,3)
local cardUserField = sub[3]:addInput()
    :setInputType("text")
    :setDefaultText("       Gustaf")
    :setInputLimit(20)
    :setSize(20,1)
    :setPosition(16,4)
sub[3]:addLabel()
    :setText("Pin eingeben:")
    :setPosition(16,8)
local cardPinField = sub[3]:addInput()
    :setInputType("password")
    :setInputLimit(4)
    :setSize(5,1)
    :setPosition(31,8)
sub[3]:addButton()
    :setText("Erstellen")
    :setPosition(20,14)
    :onClick(
        function()
            basalt.debug(utils.createCard(cardUserField.getValue(), cardPinField.getValue()))
            --local message = utils.createCard(cardUserField.getValue(), cardPinField.getValue())
            --cardResultMessage.setText(message)
            os.sleep(2)
            os.reboot()
        end)
    


basalt.autoUpdate()
