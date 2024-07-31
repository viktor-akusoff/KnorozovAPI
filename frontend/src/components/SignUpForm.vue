<script setup>
import axios from 'axios'
import { ref, computed, onMounted } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const api_address = import.meta.env.VITE_API_ADDRESS
const store = useStore()
const router = useRouter()

const login = defineModel('login')
const password = defineModel('password')
const repeat_password = defineModel('repeat_password')

const auth_user = computed(() => store.getters.USER)

let error_message = ref(null)

async function signUpUser() {
  const params = {
    login: login.value,
    password: password.value
  }

  if (!login.value) {
    error_message.value = "Login field can't be empty!"
    return
  }

  if (!password.value) {
    error_message.value = "Password field can't be empty!"
    return
  }

  if (!repeat_password.value) {
    error_message.value = 'Please, repeat your password!'
    return
  }

  if (repeat_password.value !== password.value) {
    error_message.value = 'Passwords are not the same!'
    return
  }

  await axios
    .post(api_address + '/users/signup', params)
    .then(() => {
      router.push({ name: 'login', query: { registered: 'success' } })
    })
    .catch(function (error) {
      error_message.value = error.response.data.detail
    })
}

onMounted(() => {
  if (auth_user.value) {
    router.push({ name: 'home' })
  }
})
</script>

<template>
  <div class="bg-light p-5 border border-light-subtle rounded h-25 w-50 d-flex flex-column">
    <form>
      <div class="mb-3 fs-2">SignUp to KnorozovAPI</div>
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
      <div class="input-group mb-2">
        <span class="input-group-text">Repeat password</span>
        <input
          type="password"
          v-model="repeat_password"
          name="repeat_password"
          class="form-control rounded-end"
          placeholder="Enter your password again"
        />
      </div>
      <p class="text-danger" v-if="error_message">
        {{ error_message }}
      </p>
      <button type="button" class="btn btn-primary w-100" @click="signUpUser">Sign up</button>
      <p class="mt-3">Already have an account? <router-link to="/login">Login</router-link>!</p>
    </form>
  </div>
</template>
