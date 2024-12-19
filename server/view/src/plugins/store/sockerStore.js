
import { defineStore } from "pinia";
import { onScopeDispose } from "vue";

// 加载顺序的问题
export const useSocketStore = defineStore('socket', {
    state: () =>{
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
    actions:{

        onSocketClose(){
            if (this.socket){
                this.socket.close()
            }
        },

        setupWebSocket(){
            this.socket = new WebSocket(this.address)
            this.socket.onopen = (event) => this.onSocketOpen(event)
            this.socket.onmessage = (event) => this.onSocketMessage(event)
            this.socket.onerror = (error) => this.ErrorSocket(error)
            this.socket.onclose = (event) => this.CloseSocket(event) 
        },
        CloseSocket(event){
            console.log(event)
        },
        onSocketOpen(event){
            console.log("PING")
        },
        onSocketMessage(event){
            const data = JSON.parse(event.data)
            this.data.client_status = data[0]
            this.data.client_reports = data[1]
        },
        ErrorScoket(error){
            console.log(error)
        }
        
    }
})