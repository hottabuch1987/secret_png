// composables/useWebSocket.js - ВЕРСИЯ БЕЗ ЗВОНКОВ

import { ref, computed } from 'vue'
import { useUserStore } from '~/stores/user'


export function useWebSocket() {
    const userStore = useUserStore()
    const socket = ref(null)
    const isConnected = ref(false)
    const onlineUsers = ref([])
    const messages = ref([])
    const isConnecting = ref(false)
    
    
    const connect = () => {
        const token = userStore.token
        
        if (!token) {
            console.warn('⚠️ No token available for WebSocket connection')
            return
        }
        
        if (isConnecting.value) return
        if (socket.value?.readyState === WebSocket.OPEN) return
        
        isConnecting.value = true
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
        const wsUrl = `${protocol}//localhost:8000/ws/user/?token=${token}`
        
        console.log('🔗 Connecting to WebSocket:', wsUrl)
        
        try {
            socket.value = new WebSocket(wsUrl)
            
            socket.value.onopen = () => {
                isConnected.value = true
                isConnecting.value = false
                console.log('✅ WebSocket connected successfully')
                startPingInterval()
            }
            
            socket.value.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data)
                    console.log('📨 WebSocket message received:', data.type)
                    handleMessage(data)
                } catch (error) {
                    console.error('❌ Error parsing WebSocket message:', error)
                }
            }
            
            socket.value.onclose = (event) => {
                isConnected.value = false
                isConnecting.value = false
                console.log('❌ WebSocket disconnected:', event.code, event.reason)
                stopPingInterval()
                
                setTimeout(() => {
                    if (!isConnected.value && userStore.isAuthenticated) {
                        console.log('🔄 Attempting to reconnect...')
                        connect()
                    }
                }, 3000)
            }
            
            socket.value.onerror = (error) => {
                console.error('❌ WebSocket error:', error)
                isConnecting.value = false
            }
        } catch (error) {
            console.error('❌ Failed to create WebSocket:', error)
            isConnecting.value = false
        }
    }
    
    let pingInterval = null
    
    const startPingInterval = () => {
        stopPingInterval()
        pingInterval = setInterval(() => {
            if (socket.value?.readyState === WebSocket.OPEN) {
                sendMessage('ping', {})
            }
        }, 30000)
    }
    
    const stopPingInterval = () => {
        if (pingInterval) {
            clearInterval(pingInterval)
            pingInterval = null
        }
    }
    
    const sendMessage = (type, data = {}) => {
        if (socket.value?.readyState === WebSocket.OPEN) {
            const message = { type, ...data }
            socket.value.send(JSON.stringify(message))
            return true
        }
        console.error('❌ WebSocket is not connected')
        return false
    }
    
    const getOnlineUsers = () => {
        sendMessage('get_online_users', {})
    }
    
    const disconnect = () => {
        stopPingInterval()
        
        if (socket.value) {
            socket.value.close()
            socket.value = null
        }
        
        isConnected.value = false
        isConnecting.value = false
        onlineUsers.value = []
    }
    
    const handleMessage = (data) => {
        switch (data.type) {
            case 'connection_established':
                if (data.online_users) {
                    onlineUsers.value = data.online_users
                }
                break
                
            case 'user_status_changed':
                const index = onlineUsers.value.findIndex(u => u.id === data.user_id)
                if (data.is_online) {
                    if (index === -1) {
                        onlineUsers.value.push({
                            id: data.user_id,
                            username: data.username,
                            first_name: data.first_name || '',
                            last_name: data.last_name || '',
                            avatar_url: data.avatar_url || null
                        })
                    }
                } else {
                    if (index !== -1) {
                        onlineUsers.value.splice(index, 1)
                    }
                }
                break
                
            case 'chat_message':
                messages.value.push(data.message_data)
                break
                
            case 'message_sent':
                console.log('Message sent:', data)
                break
                
            case 'pong':
                break
                
            case 'online_users_list':
                onlineUsers.value = data.online_users || []
                break
                
            default:
                console.log('Unknown message type:', data.type)
        }
    }
    
    return {
        socket,
        isConnected: computed(() => isConnected.value),
        isConnecting: computed(() => isConnecting.value),
        onlineUsers,
        messages,
        
        // Методы
        connect,
        disconnect,
        sendMessage,
        getOnlineUsers
    }
}