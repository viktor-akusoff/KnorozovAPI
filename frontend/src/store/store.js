import { createStore } from 'vuex'

const store = createStore({
  state: {
    user: JSON.parse(window.localStorage.getItem('user')),
    refresh_token: window.localStorage.getItem('refresh_token'),
    access_token: window.localStorage.getItem('access_token')
  },
  getters: {
    USER: (state) => {
      return state.user
    },
    ACCESS: (state) => {
      return state.access_token
    },
    REFRESH: (state) => {
      return state.refresh_token
    }
  },
  mutations: {
    LOGIN: (state, { user, refresh, access }) => {
      state.user = user
      window.localStorage.setItem('user', JSON.stringify(user))
      state.refresh_token = refresh
      window.localStorage.setItem('refresh_token', refresh)
      state.access_token = access
      window.localStorage.setItem('access_token', access)
    },
    LOGOUT: (state) => {
      window.localStorage.removeItem('user')
      state.user = null
      window.localStorage.removeItem('refresh_token')
      state.refresh_token = null
      window.localStorage.removeItem('access_token')
      state.access_token = null
    }
  }
})

export default store
