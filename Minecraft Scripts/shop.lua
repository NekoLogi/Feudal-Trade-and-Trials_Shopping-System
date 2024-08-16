basalt = require("basalt")
requester = require("request_handler")

ACCOUNT_PATH = "disk/account.json"
DRIVE_DIRECTION = "bottom"
pageWindow = nil
pageIndex = 1
pageGenerated = false
TEST_MODE = false
account = {
    uuid = "test",
    from = "katse2"
}

uiUsername = nil
uiBalance = nil
uiIndex = nil
uiItemName = nil
uiItemDescription = nil
uiItemPrice = nil
uiItemQuantity = nil
uiItemInput = nil


-- Logic
function diskExists()
    if disk.isPresent(DRIVE_DIRECTION) then
        return true
    end
    return false
end

function accountExists()
    if fs.exists(ACCOUNT_PATH) then
        return true
    end
    return false
end

function getDiskData()
    local file = fs.open(ACCOUNT_PATH, "r")
    local json = file.readAll()
    file.close()
    local accountData = textutils.unserialiseJSON(json)
    return accountData
end

function verifyAccount(account)
    local user = requester.get("/banking/account?uuid=" .. account.uuid .. "&from=" .. account.from)
    if user.error ~= nil then
        return nil
    end
    return user
end

function requestShopData()
    local shop = requester.get("/roller/items")
    if shop.error ~= nil then
        return nil
    end
    return shop
end

function getUserData()
    if not TEST_MODE then
        if not diskExists() then
            print("Karte einfugen um fortzufahren...")
            sleep(3)
            return nil
        end
        if not accountExists() then
            print("Karte ist korrupt oder Karte hat keine Accountdaten!")
            disk.eject()
            sleep(5)
            return nil
        end
        account = getDiskData()
    end
    local userData = verifyAccount(account)
    if userData == nil then
        print("Verifizierung fehlgeschlagen: Accountdaten stimmen nicht uberein!")
        disk.eject()
        sleep(5)
        return nil
    end
    return userData
end

function getShopData()
    local shopData = nil
    for i = 1, 3, 1 do
        shopData = requestShopData()
        if shopData ~= nil then
            return shopData
        end
        print("Verbindung zum shop fehlgeschlagen: Versuch " .. i .. " von 3")
        sleep(2)
        if i == 3 then
            print("Kontaktiere den Administrator, um das Problem zu geheben!")
            disk.eject()
            sleep(5)
            return nil
        end
    end
end

function start()
    basalt.debug()
    while true do
        term.clear()
        term.setCursorPos(1,1)
        local userData = getUserData()
        local shopData = getShopData()
        if userData and shopData then
            if not pageGenerated then
                generatePageWindow()
                pageGenerated = true
            end
            changePageValues(userData, shopData)
            break
        else
            sleep(2)
        end
    end
end

function nextPage()
    if pageIndex == 8 then
        pageIndex = 1
    else
        pageIndex = pageIndex + 1
    end
    start()
end

function prevPage()
    if pageIndex == 1 then
        pageIndex = 8
    else
        pageIndex = pageIndex - 1
    end
    start()
end

-- UI
function generatePageWindow()
    pageWindow = basalt.createFrame()
        :setBackground(colors.lightGray)
    pageWindow:addLabel()
        :setText("Shop")
        :setPosition(25,1)
        :setTextAlign("center")
    
    local frame = pageWindow:addFrame()
        :setPosition(1,2)
        :setSize("parent.w","parent.h - 1")
        :setBackground(colors.brown)
    uiUsername = frame:addLabel()
        :setPosition(15, 14)
    uiBalance = frame:addLabel()
        :setPosition(15, 16)
    uiItemName = frame:addLabel()
        :setPosition(2, 3)
        :setSize(49,2)
        :setTextAlign("center")
        :setBackground(colors.white)
    frame:addLabel()
        :setPosition(2, 2)
        :setText("")
        :setSize(49,1)
        :setTextAlign("center")
        :setBackground(colors.white)
    uiItemDescription = frame:addLabel()
        :setPosition(2, 6)
        :setSize(30,7)
        :setBackground(colors.black)
        :setForeground(colors.white)
    uiItemQuantity = frame:addLabel()
        :setPosition(33, 6)
        :setSize(18,1)
        :setBackground(colors.black)
        :setForeground(colors.white)
    uiItemPrice = frame:addLabel()
        :setPosition(33, 7)
        :setSize(18,1)
        :setBackground(colors.black)
        :setForeground(colors.white)
    frame:addLabel()
        :setPosition(33, 9)
        :setSize(13,1)
        :setTextAlign("center")
        :setText("Menge: ")
    uiItemInput = frame:addInput()
        :setPosition(42, 9)
        :setSize(3,1)
        :setBackground(colors.black)
        :setForeground(colors.white)
        :setInputLimit(2)
        :setTextOffset(2)
        :setInputType("number")
    frame:addLabel()
        :setPosition(42, 9)
        :setSize(14,1)
        :setTextAlign("center")
        :setText("Stk.")
    local buyButton = frame:addButton()
        :setText("Kaufen")
        :setPosition(37, 11)
        :setSize(10,1)
        :setBackground(colors.green)
        :onClick(function(self,event,button,x,y)
            buy()
        end)
    uiIndex = frame:addLabel()
        :setPosition(1, 18)
        :setTextAlign("center")
        :setSize(51,1)
        :setBackground(colors.black)
        :setForeground(colors.white)
    local nextButton = frame:addButton()
        :setText("Next")
        :setPosition(39, 14)
        :onClick(function(self,event,button,x,y)
            nextPage()
        end)
    local prevButton = frame:addButton()
        :setText("Prev")
        :setPosition(2, 14)
        :onClick(function(self,event,button,x,y)
            prevPage()
        end)
end

function changePageValues(userData, shopData)
    uiUsername:setText("User: " .. userData.from)
    uiBalance:setText(userData.currency .. ": " .. userData.balance)
    uiIndex:setText("-------- " .. pageIndex .. " ---------")
    
    uiItemName:setText(shopData[pageIndex].display_name)
    uiItemPrice:setText("\n " .. shopData[pageIndex].currency .. ": " .. shopData[pageIndex].price)
    uiItemDescription:setText(shopData[pageIndex].description)
    uiItemQuantity:setText("\n Menge: " .. shopData[pageIndex].amount .. " Stk")
end

function buy()
    if tonumber(uiItemInput:getValue()) == nil then
        basalt.debug("Menge eingeben!")
        return
    end
    if tonumber(uiItemInput:getValue()) > 64 then
        basalt.debug("Max. Menge ist 64x")
        return
    end
    if tonumber(uiItemInput:getValue()) < 1 then
        basalt.debug("Min. Menge ist 1x")
        return
    end

    local userData = getUserData()
    if userData == nil then
        basalt.debug("Karte nicht erkannt.")
        return
    end
    local jsonData = {
        uuid = userData.uuid,
        from = userData.from,
        amount = uiItemInput:getValue(),
        id = getShopData()[pageIndex].id
    }
    local requester = require("request_handler")
    local json = requester.pairsToJson(jsonData)
    local item = requester.put("/roller/item/purchase", json)
    if item.error ~= nil then
        basalt.debug(item.error)
        return
    end
    commands.exec(item.command)

    changePageValues(getUserData(), getShopData())
end


-- Start
start()
basalt.autoUpdate()