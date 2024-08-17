M = {}

function M.pairsToJson(data)
    return textutils.serialiseJSON(data)
end

function M.request(url, method, json)
    local newUrl = "http://127.0.0.1:5000" .. url
    http.request({
        url = newUrl,
        body = json,
        headers = {["Content-Type"] = "application/json"},
        method = method
    })
    
    local event, url, handle
    repeat
        event, url, handle = os.pullEvent("http_success")
    until url == newUrl
    local response = handle.readAll()
    handle.close()
    return textutils.unserialiseJSON(response)
end

function M.get(url)
    return M.request(url, "GET", nil)
end

function M.post(url, json)
    return M.request(url, "POST", json)
end

function M.put(url, json)
    return M.request(url, "PUT", json)
end

function M.delete(url)
    return M.request(url, "DELETE", nil)
end

return M