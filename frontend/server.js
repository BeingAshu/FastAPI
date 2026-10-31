
const http = require("http");
const fs = require("fs");
const path = require("path");

const PORT = 5500;
const frontendPath = __dirname;

const mimeTypes = {
    ".html": "text/html",
    ".css": "text/css",
    ".js": "application/javascript",
    ".json": "application/json"
};

http.createServer((req, res) => {

    const url = new URL(req.url, `http://localhost:${PORT}`);

    let requestedPath = decodeURIComponent(url.pathname);

    if (requestedPath === "/") {
        requestedPath = "/login.html";
    }

    const filePath = path.resolve(frontendPath, "." + requestedPath);

    if (filePath !== frontendPath &&
        !filePath.startsWith(frontendPath + path.sep)) {
        res.writeHead(403);
        return res.end("Forbidden");
    }

    fs.readFile(filePath, (err, data) => {

        if (err) {
            res.writeHead(404, {
                "Content-Type": "text/plain"
            });
            return res.end("Not Found");
        }

        const contentType =
            mimeTypes[path.extname(filePath)] || "application/octet-stream";

        res.writeHead(200, {
            "Content-Type": contentType
        });

        res.end(data);
    });

}).listen(PORT, () => {
    console.log(`Frontend running at http://127.0.0.1:${PORT}`);
});
