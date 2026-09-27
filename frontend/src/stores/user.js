// stores/user.js
import { defineStore } from 'pinia'
import axios from 'axios'

export const useUserStore = defineStore({
    id: 'user',

    state: () => ({
        user: {
            id: null,
            username: null,
            email: null,
            token: null,
            first_name: null,
            last_name: null,
            email_confirmed: false,
            avatar_url: null,  
            photos: [],        
        },
        isAuthenticated: false,
    }),

    getters: {
        // 🔥 ДОБАВЛЯЕМ ГЕТТЕР ДЛЯ ТОКЕНА
        token: (state) => state.user.token,
        
        fullName: (state) => {
            const first = state.user.first_name || ''
            const last = state.user.last_name || ''
            return first || last ? `${first} ${last}`.trim() : state.user.username || ''
        },
        userInitials: (state) => {
            const name = state.fullName
            if (name && name !== state.user.username) {
                const names = name.split(' ')
                return names.map(n => n[0]).join('').toUpperCase().slice(0, 2)
            }
            return state.user.username ? state.user.username[0].toUpperCase() : '?'
        },
        avatar: (state) => {
            return state.user.avatar_url || null
        },
        userPhotos: (state) => {
            return state.user.photos || []
        }
    },

    actions: {
        initStore() {
            const token = localStorage.getItem('user.token')
            if (token) {
                this.user.token = token
                this.user.id = localStorage.getItem('user.id') || null
                this.user.username = localStorage.getItem('user.username') || null
                this.user.email = localStorage.getItem('user.email') || null
                this.user.first_name = localStorage.getItem('user.first_name') || null
                this.user.last_name = localStorage.getItem('user.last_name') || null
                this.user.email_confirmed = localStorage.getItem('user.email_confirmed') === 'true'
                this.user.avatar_url = localStorage.getItem('user.avatar_url') || null
                
                try {
                    const photos = localStorage.getItem('user.photos')
                    this.user.photos = photos ? JSON.parse(photos) : []
                } catch {
                    this.user.photos = []
                }
                
                this.isAuthenticated = true
                axios.defaults.headers.common['Authorization'] = `Token ${token}`
            }
        },

        setToken(data) {
            const token = data.auth_token || data.token || data
            this.user.token = token
            this.isAuthenticated = true
            localStorage.setItem('user.token', token)
            axios.defaults.headers.common['Authorization'] = `Token ${token}`
        },

        removeToken() {
            this.user.token = null
            this.user.id = null
            this.user.username = null
            this.user.email = null
            this.user.first_name = null
            this.user.last_name = null
            this.user.email_confirmed = false
            this.user.avatar_url = null
            this.user.photos = []
            this.isAuthenticated = false

            const keys = [
                'user.token', 'user.id', 'user.username', 'user.email',
                'user.first_name', 'user.last_name', 'user.email_confirmed', 
                'user.avatar_url', 'user.photos'
            ]
            keys.forEach(key => localStorage.removeItem(key))
            delete axios.defaults.headers.common['Authorization']
        },

        setUserInfo(user) {
            this.user.id = user.id
            this.user.username = user.username
            this.user.email = user.email
            this.user.first_name = user.first_name || ''
            this.user.last_name = user.last_name || ''
            this.user.email_confirmed = user.email_confirmed || false
            this.user.avatar_url = user.avatar_url || null
            this.user.photos = user.photos || []
            this.isAuthenticated = true

            localStorage.setItem('user.id', this.user.id)
            localStorage.setItem('user.username', this.user.username)
            localStorage.setItem('user.email', this.user.email)
            localStorage.setItem('user.first_name', this.user.first_name)
            localStorage.setItem('user.last_name', this.user.last_name)
            localStorage.setItem('user.email_confirmed', String(this.user.email_confirmed))
            
            if (this.user.avatar_url) {
                localStorage.setItem('user.avatar_url', this.user.avatar_url)
            } else {
                localStorage.removeItem('user.avatar_url')
            }
            
            localStorage.setItem('user.photos', JSON.stringify(this.user.photos))
        },

        updateUserInfo(userData) {
            Object.keys(userData).forEach(key => {
                if (key in this.user) {
                    this.user[key] = userData[key]
                    
                    if (key === 'email_confirmed') {
                        localStorage.setItem('user.email_confirmed', String(userData[key]))
                    } else if (key === 'avatar_url') {
                        if (userData[key]) {
                            localStorage.setItem('user.avatar_url', userData[key])
                        } else {
                            localStorage.removeItem('user.avatar_url')
                        }
                    } else if (key === 'photos') {
                        localStorage.setItem('user.photos', JSON.stringify(userData[key]))
                    } else {
                        localStorage.setItem(`user.${key}`, userData[key] || '')
                    }
                }
            })
        },

        async fetchUserInfo() {
            try {
                const response = await axios.get('/auth/users/me/')
                this.setUserInfo(response.data)
                return response.data
            } catch (error) {
                console.error('Error fetching user info:', error)
                if (error.response && error.response.status === 401) {
                    this.removeToken()
                }
                throw error
            }
        }
    }
})