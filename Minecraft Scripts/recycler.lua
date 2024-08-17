local requester = require("request_handler")
local file_path = "disk/account.json"
monitor = peripheral.wrap("top")
monitor.setTextScale(0.5)
monitor.clear()

diskPosition = "front"

local function monPrint(message)
    monitor.scroll(-1)
    monitor.setCursorPos(1, 1)
    monitor.write(message)
    print(message)
end

local function monClear()
    monitor.clear()
end

local function recycle(accountData)
    for i = 1, 16 do
        turtle.select(i)
        local item = turtle.getItemDetail()
        if item ~= nil then
            local jsonData = {
                uuid = accountData.uuid,
                from = accountData.from,
                name = item.name,
                amount = item.count
            }
            local json = requester.pairsToJson(jsonData)
            local result = requester.put("/shop/recycle", json)
            monPrint("--------------------------------")
            if result.error ~= nil then
                monPrint("# " .. result.error .. " @".. jsonData.name)
                turtle.turnLeft()
                turtle.drop()
                turtle.turnRight()
            else
                monPrint("  Added: " .. result.price .. " " .. result.currency)
                monPrint("- Recycled: " .. result.display_name .. " " .. result.amount .. "x")
                turtle.dropDown()
            end
        end
    end
end

monPrint("Resetting turtle...")
while not redstone.getInput("back") do
    turtle.turnLeft()
end
monPrint("Turtle resetted!")
::reboot::
monClear()
while true do
    monPrint("Checking for Card...")
    local accountData = nil
    if disk.isPresent(diskPosition) then
        if fs.exists(file_path) then
            monPrint("Reading card data...")
            local file = fs.open(file_path, "r")
            local json = file.readAll()
            file.close()
            accountData = textutils.unserialiseJSON(json)
        end
        if accountData == nil then
            monPrint("Failed to read card data!")
            os.sleep(5)
            goto reboot
        end
        local user = requester.get("/banking/account?uuid=" .. accountData.uuid .. "&from=" .. accountData.from)
        if user.error ~= nil then
            monPrint("Failed to login: " .. user.error)
            os.sleep(5)
            goto reboot
        end
        monPrint("Logged in with " .. user.from)


        while true do
            if not disk.isPresent(diskPosition) then
                goto reboot
            end        
            recycle(accountData)
            os.sleep(3)
        end
    else
        monClear()
        monPrint("No cart detected!")
    end
    os.sleep(3)
end