local basalt = require("basalt") -- we need basalt here
local requester = require("request_handler")


diskPosition = "bottom"
FILE_PATH = "disk/account.json"

local function createCard(username, pin)
    if not disk.isPresent(diskPosition) then
        return "Insert disk and try again!"
    end
    local jsonData = {
        from = username,
        pin = pin
    }
    local json = requester.pairsToJson(jsonData)
    local user = requester.post("/banking/card", json)
    local file = fs.open(FILE_PATH, "w")
    if user.error ~= nil then
        return user.error
    end
    disk.setLabel(diskPosition, user.from .. " : " .. user.id)
    file.write(requester.pairsToJson({uuid = user.uuid, from = user.from, id = user.id}))
    file.close()
    return "Card created successfully, take from drive."
end

local function createAccount(username, pin)
    if not disk.isPresent(diskPosition) then
        return "Insert disk and try again!"
    end
    local jsonData = {
        from = username,
        pin = pin
    }
    local json = requester.pairsToJson(jsonData)
    local user = requester.post("/banking/account", json)
    if user.error ~= nil then
        return nil
    end
    return user
end

local function getAccount()
    if not disk.isPresent(diskPosition) then
        return "Insert disk and try again!"
    end
    local accountData = nil
    if fs.exists(FILE_PATH) then
        local file = fs.open(FILE_PATH, "r")
        local json = file.readAll()
        file.close()
        accountData = textutils.unserialiseJSON(json)
    end
    if accountData == nil then
        return "Failed to read card data!"
    end
    local user = requester.get("/banking/account?uuid=" .. accountData.uuid .. "&from=" .. accountData.from)
    if user.error ~= nil then
        return "Failed to login: " .. user.error
    end
    return "Balance: " .. user.balance .. " " .. user.currency
end

local function deleteAccount(pin)
    if not disk.isPresent(diskPosition) then
        return "Insert disk and try again!"
    end
    local accountData = nil
    if fs.exists(FILE_PATH) then
        local file = fs.open(FILE_PATH, "r")
        local json = file.readAll()
        file.close()
        accountData = textutils.unserialiseJSON(json)
    end
    if accountData == nil then
        return "Failed to read card data!"
    end
    local user = requester.delete("/banking/account?uuid=" .. accountData.uuid .. "&from=" .. accountData.from .. "&pin=" .. pin)
    if user.error ~= nil then
        return "Failed to login: " .. user.error
    end
    return "Account '" .. accountData.from .. "' deleted!"
end




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
    :setText("Navigieren konnen Sie mit den Tabs oben angezeigt.")
    :setPosition(2,8)
sub[1]:addLabel()
    :setText("[Account]: Hier konnen Sie ein Konto erstellen")
    :setPosition(1,10)
sub[1]:addLabel()
    :setText("und Kontodaten verwalten.")
    :setPosition(12,11)
sub[1]:addLabel()
    :setText("[Karte]: Hier konnen Sie eine verlorene Karte")
    :setPosition(1,12)
sub[1]:addLabel()
    :setText("erstellen, sofern Sie die Daten kennen.")
    :setPosition(10,13)

sub[2]:addLabel()
    :setText("Wahle eine Option:")
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
                        local user = createAccount(accountUserField.getValue(), accountPinField.getValue())
                        if user ~= nil then
                            basalt.debug(createCard(user.from, user.pin))
                        else
                            basalt.debug("Failed to create account, check your input!")
                        end
                        createFrame:hide()
                    end)
        end)
sub[2]:addButton()
    :setText("Kontostand")
    :setPosition(20,9)
    :onClick(
        function()
            basalt.debug(getAccount())
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
            basalt.debug(createCard(cardUserField.getValue(), cardPinField.getValue()))
        end)
    


basalt.autoUpdate()