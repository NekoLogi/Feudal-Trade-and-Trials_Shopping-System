M = {}


function M.createFrames()
    local file_path = "disk/account.json"
    if not disk.isPresent("left") then
        return "Insert disk and try again!"
    end
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
            :setSize(2,20)
    end
    
    
    local jsonData = {
        username = username,
        password = pin
    }
    local json = requester.pairsToJson(jsonData)
end

function M.createAccount(username, pin)
    local file_path = "disk/account.json"
    if not disk.isPresent("left") then
        return { nil, "Insert disk and try again!"}
    end
    local jsonData = {
        username = username,
        password = pin
    }
    local requester = require("request_handler")
    local json = requester.pairsToJson(jsonData)
    local user = requester.post("http://127.0.0.1:5000/banking/account", json)
    if user.error ~= nil then
        return {nil, user.error}
    end
    return {username, pin}
end

function M.getAccount()
    local file_path = "disk/account.json"
    if not disk.isPresent("left") then
        return "Insert disk and try again!"
    end
    local accountData = nil
    if fs.exists(file_path) then
        local file = fs.open(file_path, "r")
        local json = file.readAll()
        file.close()
        accountData = textutils.unserialiseJSON(json)
    end
    if accountData == nil then
        return "Failed to read card data!"
    end
    local requester = require("request_handler")
    local user = requester.get("http://127.0.0.1:5000/banking/account?uuid=" .. accountData.uuid .. "&username=" .. accountData.from_name)
    if user.error ~= nil then
        return "Failed to login: " .. user.error
    end
    return "Balance: " .. user.balance .. " " .. user.currency_name
end


return M