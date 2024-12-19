import { defineStore } from 'pinia';

export const useSocketStore = defineStore('socket', {
    state: () => {
        return {
            socket: null,
            address: "http://localhost:8000/ws",
            lockreconnect: false,
            reconnInterval: 3000,
            data: {
                client_status: null,
                client_reports: null,
            }
        }
    },
    actions: {
        onSocketClose() {
            if (this.socket) {
                this.socket.close();
            }
        },

        setupWebSocket() {
            const init = (address) => {
                const socket = new WebSocket(address);
                socket.onopen = this.onSocketOpen;
                socket.onmessage = this.onSocketMessage;
                socket.onerror = this.onErrorSocket;
                socket.onclose = this.onSocketClose;
                return socket;
            };

            this.socket = init(this.address);
        },

        onSocketOpen(e) {
            console.log(e);
        },

        onSocketMessage(e) {
            const data = JSON.parse(e.data);
            this.data.client_status = data[0];
            this.data.client_reports = data[1];
        },

        onErrorSocket(error) {
            console.error('WebSocket error:', error);
        },

        onSocketClose() {
            if (this.socket) {
                this.socket.close();
            }
        }
    }
});
