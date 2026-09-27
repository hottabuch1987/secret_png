import axios from "axios"

export default defineNuxtPlugin((nuxtApp) => {
    const config = useRuntimeConfig()
    axios.defaults.baseURL = config.public.apiBase
    axios.defaults.withCredentials = true;

    return {
        provide: { 
            axios: axios
        },
    }
})