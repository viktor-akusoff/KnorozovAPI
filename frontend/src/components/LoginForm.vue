<script setup>
import axios from 'axios'
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter, useRoute } from 'vue-router'

const api_address = import.meta.env.VITE_API_ADDRESS
const store = useStore()
const router = useRouter()
const route = useRoute()

const login = defineModel('login')
const password = defineModel('password')

const auth_user = computed(() => store.getters.USER)

const registered = ref(route.query.registered === 'success')
const changed_password = ref(route.query.changed_password === 'success')

let error_message = ref(null)

async function authUser() {
  const params = new FormData()
  params.append('username', login.value)
  params.append('password', password.value)

  let access = ''
  let refresh = ''
  let user = {}

  if (!login.value) {
    error_message.value = "Login field can't be empty!"
    return
  }

  if (!password.value) {
    error_message.value = "Password field can't be empty!"
    return
  }

  await axios
    .post(api_address + '/users/login', params)
    .then((response) => {
      access = response.data.access_token
      refresh = response.data.refresh_token
    })
    .catch(function (error) {
      error_message.value = error.response.data.detail
      registered.value = null
    })

  await axios
    .get(api_address + `/users/${login.value}`)
    .then((response) => {
      user = response.data
    })
    .catch(function (error) {
      console.error(error)
    })

  if (user && refresh && access) {
    store.commit('LOGIN', { user, refresh, access })
    router.push({ name: 'home' })
  }
}

onMounted(() => {
  if (auth_user.value) {
    router.push({ name: 'home' })
  }
})
</script>

<template>
  <div
    class="bg-light p-5 border border-light-subtle rounded h-25 w-50 d-flex flex-column justify-content-center"
  >
    <form>
      <div class="mb-3 fs-2">Login to KnorozovAPI</div>
      <p class="text-success" v-if="registered">
        You've been successfully registered! Now you can login.
      </p>
      <p class="text-success" v-if="changed_password">
        You've successfully changed your password! Now you must re-login.
      </p>
      <div class="input-group mb-2">
        <span class="input-group-text">Login</span>
        <input
          type="text"
          v-model="login"
          name="login"
          class="form-control rounded-end"
          placeholder="Enter your username"
        />
      </div>
      <div class="input-group mb-2">
        <span class="input-group-text">Password</span>
        <input
          type="password"
          v-model="password"
          name="password"
          class="form-control rounded-end"
          placeholder="Enter your password"
        />
      </div>
      <p class="text-danger" v-if="error_message">
        {{ error_message }}
      </p>
      <button type="button" class="btn btn-primary w-100" @click="authUser">Login</button>
      <p class="mt-3">Don't have an account? <router-link to="/signup">Sign up</router-link>!</p>
    </form>
  </div>
</template>
