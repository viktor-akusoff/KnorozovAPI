<script setup>
import axios from 'axios'
import { defineProps, defineModel, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

const store = useStore()
const router = useRouter()

const props = defineProps({
  auth_user: String
})

const api_address = import.meta.env.VITE_API_ADDRESS

const old_password = defineModel('old_password')
const old_password_err = ref('')

const new_password = defineModel('new_password')
const new_password_err = ref('')

const repeat_password = defineModel('repeat_password')
const repeat_password_err = ref('')

const not_same_password_err = ref('')

function checkPassword() {
  const params = new FormData()
  params.append('username', props.auth_user.login)
  params.append('password', old_password.value)

  return axios
    .post(api_address + '/users/login', params)
    .then(() => true)
    .catch(() => false)
}

async function changePassword() {
  old_password_err.value = ''
  new_password_err.value = ''
  repeat_password_err.value = ''
  not_same_password_err.value = ''

  if (!old_password.value) {
    old_password_err.value = 'Please, enter your old password.'
    return
  }

  if (!new_password.value) {
    new_password_err.value = 'Please, enter your new password.'
    return
  }

  if (!repeat_password.value) {
    repeat_password_err.value = 'Please, re-enter your new password.'
    return
  }

  if (repeat_password.value !== new_password.value) {
    not_same_password_err.value = "Passwords don't match!"
    return
  }

  checkPassword().then((response) => {
    if (!response) {
      old_password_err.value = 'Wrong password!'
    } else {
      let params = {
        password: new_password.value
      }
      let config = {
        headers: {
          Authorization: `Bearer ${store.getters.ACCESS}`
        }
      }
      axios.put(api_address + '/users/update_password', params, config).then(() => {
        store.commit('LOGOUT')
        router.push({ name: 'login', query: { changed_password: 'success' } })
      })
    }
  })
}
</script>

<template>
  <div v-if="auth_user" class="d-flex flex-row">
    <p class="me-2">Roles available:</p>
    <p v-if="auth_user.roles.includes('admin')">You're an admin user!</p>
    <p v-else v-for="(role, index) in auth_user.roles" :key="index" class="me-2">{{ role }}</p>
  </div>
  <div>
    <input
      type="password"
      class="form-control mb-2"
      placeholder="Enter your old password."
      v-model="old_password"
    />
    <p class="text-danger" v-if="old_password_err">{{ old_password_err }}</p>
    <input
      type="password"
      class="form-control mb-2"
      placeholder="Enter your new password."
      v-model="new_password"
    />
    <p class="text-danger" v-if="new_password_err">{{ new_password_err }}</p>
    <input
      type="password"
      class="form-control mb-2"
      placeholder="Enter repeat your new password."
      v-model="repeat_password"
    />
    <p class="text-danger" v-if="repeat_password_err">{{ repeat_password_err }}</p>
    <p class="text-danger" v-if="not_same_password_err">{{ not_same_password_err }}</p>
    <button class="btn btn-primary w-100" @click="changePassword()">Change password</button>
  </div>
</template>
