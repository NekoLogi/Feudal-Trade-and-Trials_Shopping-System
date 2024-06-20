M = {}

function M.createCard(username, pin)
    local file_path = "disk/account.json"
    if not disk.isPresent("left") then
        return "Insert disk and try again!"
    end
    local jsonData = {
        username = username,
        password = pin
    }
    local requester = require("request_handler")
    local json = requester.pairsToJson(jsonData)
    local user = requester.post("http://127.0.0.1:5000/banking/card", json)
    local file = fs.open(file_path, "w")
    if user.error ~= nil then
        return user.error
    end
    disk.setLabel("left", user.username .. " : " .. user.id)
    file.write(requester.pairsToJson({uuid = user.uuid, from_name = user.username, id = user.id}))
    file.close()
    return "Card created successfully, take from drive."
end

function M.createAccount(username, pin)
    local file_path = "disk/account.json"
    if not disk.isPresent("left") then
        return "Insert disk and try again!"
    end
    local jsonData = {
        username = username,
        password = pin
    }
    local requester = require("request_handler")
    local json = requester.pairsToJson(jsonData)
    local user = requester.post("http://127.0.0.1:5000/banking/account", json)
    if user.error ~= nil then
        return user.error
    end

    return M.createCard(username, pin)
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
