
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
                client_waitdone: null,  
                softwarelist: null,
                
            }
        }
    },
    getters:{
        format_waitdone(state){
            const waitdones = []
            for(const item in state.data.client_waitdone){
                const waitdone = JSON.parse(item)
                waitdones.push((waitdone.label, waitdone.data))
                console.log(waitdone)
            }
            return waitdones
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
            this.data.client_waitdone = data[2]
            this.data.softwarelist = data[3]
            // console.log(data)
        },
        ErrorScoket(error){
            console.log(error)
        }
        
    }
})