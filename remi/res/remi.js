class Remi {
    constructor() {
        this._pendingSendMessages = [];
        this._ws = null;
        this._comTimeout = null;
        this._failedConnections = 0;
        this._openSocket();
    }

    _byteLength(str) {
        return new TextEncoder().encode(str).length;
    }

    _paramPacketize(params) {
        return Object.entries(params)
            .map(([key, value]) => `${this._byteLength(`${key}=${value}`)}|${key}=${value}`)
            .join('|');
    }

    _openSocket() {
        const wsProtocol = location.protocol.startsWith('https') ? 'wss' : 'ws';
        this._ws = new WebSocket(`${wsProtocol}://${RemiSettings.host}/`);
        console.debug('Opening WebSocket');

        this._ws.onopen = () => this._handleOpen();
        this._ws.onmessage = (evt) => this._handleMessage(evt);
        this._ws.onclose = (evt) => this._handleClose(evt);
        this._ws.onerror = (evt) => console.debug(`WebSocket error: ${evt.reason}`);
    }

    _handleOpen() {
        if (this._ws.readyState === WebSocket.OPEN) {
            this._ws.send('connected');
            document.getElementById("loading")?.style?.display = 'none';
            this._failedConnections = 0;
            while (this._pendingSendMessages.length) {
                this._ws.send(this._pendingSendMessages.shift());
            }
        } else {
            console.debug('WebSocket opened, but not ready.');
        }
    }

    _handleMessage(evt) {
        const msg = evt.data;
        if (msg.startsWith('0')) {
            document.body.innerHTML = decodeURIComponent(msg.slice(msg.indexOf(',') + 1));
        } else if (msg.startsWith('1')) {
            this._updateWidget(msg);
        } else if (msg.startsWith('2')) {
            try {
                eval(msg.slice(1));
            } catch (e) {
                console.debug(e.message);
            }
        } else if (msg.startsWith('3')) {
            this._pendingSendMessages.shift();
            clearTimeout(this._comTimeout);
        }
    }

    _updateWidget(msg) {
        let [idElem, ...content] = msg.slice(2).split(',');
        const elem = document.getElementById(idElem);
        if (elem) {
            elem.insertAdjacentHTML('afterend', decodeURIComponent(content.join(',')));
            elem.remove();
        }
    }

    _handleClose(evt) {
        console.debug(`WebSocket closed: ${evt.code}, reason: ${evt.reason}`);
        document.getElementById("loading")?.style?.display = '';
        this._failedConnections++;

        if (this._failedConnections > 3) {
            fetch(location.href, { method: 'HEAD' })
                .then(response => response.ok && location.reload());
            this._failedConnections = 0;
        }
        if (evt.code === 1006) this._renewConnection();
    }

    sendCallbackParam(widgetID, functionName, params = {}) {
        const message = encodeURIComponent(`callback/${widgetID}/${functionName}/${this._paramPacketize(params)}`);
        this._pendingSendMessages.push(message);
        if (this._pendingSendMessages.length < RemiSettings.maxPendingMessages && this._ws?.readyState === WebSocket.OPEN) {
            this._ws.send(message);
            this._comTimeout ??= setTimeout(() => this._checkTimeout(), RemiSettings.messagingTimeout);
        } else {
            console.debug('Reconnecting WebSocket');
            this._renewConnection();
        }
    }

    sendCallback(widgetID, functionName) {
        this.sendCallbackParam(widgetID, functionName);
    }

    _renewConnection() {
        if (this._ws?.readyState === WebSocket.OPEN) {
            this._ws.close();
        } else if (this._ws?.readyState > WebSocket.CONNECTING) {
            this._openSocket();
        }
    }

    _checkTimeout() {
        if (this._pendingSendMessages.length) this._renewConnection();
    }

    uploadFile(widgetID, eventSuccess, eventFail, eventData, file) {
        const xhr = new XMLHttpRequest();
        xhr.upload.onprogress = (e) => {
            if (e.lengthComputable) {
                this.sendCallbackParam(widgetID, 'onprogress', {
                    filename: file.name,
                    loaded: e.loaded,
                    total: e.total
                });
            }
        };
        xhr.open('POST', '/');
        xhr.setRequestHeader('filename', file.name);
        xhr.setRequestHeader('listener', widgetID);
        xhr.setRequestHeader('listener_function', eventData);

        xhr.onload = () => {
            if (xhr.status === 200) {
                this.sendCallbackParam(widgetID, eventSuccess, { filename: file.name });
            } else if (xhr.status === 400) {
                this.sendCallbackParam(widgetID, eventFail, { filename: file.name });
            }
        };
        
        const fd = new FormData();
        fd.append('upload_file', file);
        xhr.send(fd);
    }
}

window.onerror = (message, source, lineno, colno, error) => {
    remi.sendCallbackParam(RemiSettins.emitterIdentifier, RemiSettings.eventName, {
        message,
        source,
        lineno,
        colno,
        error: JSON.stringify(error)
    });
    return false;
};

window.remi = new Remi();
