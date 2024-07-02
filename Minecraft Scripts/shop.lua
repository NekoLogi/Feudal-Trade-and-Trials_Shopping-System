basalt = require("basalt")


local function createFrames(uuid, username)
    local requester = require("request_handler")
    
    -- Get user data.
    local user = requester.get("http://127.0.0.1:5000/banking/account?uuid=" .. uuid .. "&username=" .. username)
    if user.error ~= nil then
        return user.error
    end

    -- Get shop items.
    local shop = requester.get("http://localhost:5000/shop/items")
    if shop.error ~= nil then
        return shop.error
    end

    -- create panes
    for k, v in pairs(shop) do
        local pane = sub:addPane()
            :setBackground(colors.brown)
            :setPosition(1,1)
            :setSize(2,20*k)
            :addLabel()
            :setText(v.displayname)
            :setPosition(4,20*k)
            :addLabel()
            :setText(v.currency .. " " .. v.currencyname)
            :setPosition(4,(20*k)+1)

    end
end


local main = basalt.createFrame()
    :setTheme({
        FrameBG = colors.brown,
        FrameFG = colors.white})

sub = main:addFrame()
    :setPosition(1, 2)
    :setSize("parent.w", "parent.h - 1")

createFrames("test", "katse2")

local function getDisk()
    local file_path = "disk/account.json"
    if not disk.isPresent("left") then
        return "Insert disk and try again!"
    end
    if fs.exists(file_path) then
        local file = fs.open(file_path, "r")
        local json = file.readAll()
        file.close()
        accountData = textutils.unserialiseJSON(json)
    end
    if accountData == nil then
        return {nil, "Failed to read card data!"}
    end
    local user = requester.get("http://127.0.0.1:5000/banking/account?uuid=" .. accountData.uuid .. "&username=" .. accountData.from_name)
    if user.error ~= nil then
        return {nil, "Failed to login: " .. user.error}
    end
    return {accountData, "Welcome " .. accountData.from_name}
end



basalt.autoUpdate()