M = {}

function M.pairsToJson(data)
    return textutils.serialiseJSON(data)
end

function M.request(myUrl, method, json)
    http.request({
        url = myUrl,
        body = json,
        headers = {["Content-Type"] = "application/json"},
        method = method
    })
    
    local event, url, handle
    repeat
        event, url, handle = os.pullEvent()
        if event == "http_failure" and url == myUrl then
            print("HTTP request failed")
        end
    until event == "http_success" and url == myUrl

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

function M.delete(url, json)
    return M.request(url, "DELETE", json)
end

return M