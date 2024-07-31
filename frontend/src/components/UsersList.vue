<script setup>
import axios from 'axios'
import { ref, onMounted, reactive, defineModel, computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

const api_address = import.meta.env.VITE_API_ADDRESS

const users = defineModel('users')
const languages = defineModel('languages')

const searchField = defineModel('searchField')

const selectedLanguages = reactive({})

async function loadUsersList() {
  let config = {
    headers: {
      Authorization: `Bearer ${store.getters.ACCESS}`
    }
  }
  await axios
    .get(api_address + '/users', config)
    .then((response) => {
      users.value = response.data.filter((user) => !user.roles.includes('admin'))
      users.value.forEach((user) => {
        selectedLanguages[user.login] = {}
        selectedLanguages[user.login]['old_value'] = {}
        selectedLanguages[user.login]['new_value'] = {}
        languages.value.forEach((language) => {
          const current_role = user.roles.includes(language.code)
          selectedLanguages[user.login]['old_value'][language.code] = current_role
          selectedLanguages[user.login]['new_value'][language.code] = current_role
        })
      })
    })
    .catch((error) => {
      console.log(error)
    })
}

async function loadLanguagesList() {
  await axios
    .get(api_address + '/translations/languages')
    .then((response) => {
      languages.value = response.data
    })
    .catch((error) => {
      console.log(error.response.data.detail)
    })
}

async function updateRoles(login) {
  const { new_value } = selectedLanguages[login]

  let roles = []

  for (const [key, value] of Object.entries(new_value)) {
    if (value) {
      roles.push(key)
    }
  }

  if (!confirm(`Are you sure that you want to change roles for "${login}"?`)) {
    return
  }

  let config = {
    headers: {
      Authorization: `Bearer ${store.getters.ACCESS}`
    }
  }

  let params = {
    codes: roles
  }

  await axios
    .put(api_address + `/users/${login}/set_roles`, params, config)
    .then(() => {
      loadData()
    })
    .catch((error) => {
      console.log(error.response.data.detail)
    })
}

function filterUsers() {
  if (!searchField.value) {
    return users.value
  }
  let result = users.value.filter((user) => {
    return user.login.toLowerCase().indexOf(searchField.value.toLowerCase()) != -1
  })
  return result
}

async function deleteUser(login) {
  if (!confirm(`Are you sure that you want to delete "${login}"?`)) {
    return
  }

  let config = {
    headers: {
      Authorization: `Bearer ${store.getters.ACCESS}`
    }
  }

  await axios
    .delete(api_address + `/users/${login}/delete`, config)
    .then(() => {
      loadData()
    })
    .catch((error) => {
      console.log(error.response.data.detail)
    })
}

async function loadData() {
  await loadLanguagesList()
  await loadUsersList()
}

const filtered_users = computed(() => filterUsers())

onMounted(() => {
  loadData()
})
</script>

<template>
  <input class="form-control mb-2" type="text" placeholder="Search users" v-model="searchField" />
  <table class="table table-light table-striped table-hover rounded">
    <thead class="table-dark">
      <tr>
        <th scope="col">Login</th>
        <th scope="col">Roles</th>
        <th></th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(user, index) in filtered_users" :key="index">
        <td class="text-center">{{ user.login }}</td>
        <td>
          <div class="btn-group" role="group" v-if="selectedLanguages[user.login]">
            <template v-for="(language, index) in languages" :key="index">
              <input
                type="checkbox"
                class="btn-check"
                :id="`${user.login}-${language.code}`"
                autocomplete="off"
                v-model="selectedLanguages[user.login].new_value[language.code]"
              />
              <label class="btn btn-dark" :for="`${user.login}-${language.code}`">{{
                language.code
              }}</label>
            </template>
          </div>
        </td>
        <td>
          <button
            v-if="selectedLanguages[user.login]"
            @click="updateRoles(user.login)"
            class="btn btn-primary w-100"
            :class="{
              disabled:
                JSON.stringify(selectedLanguages[user.login].new_value) ==
                JSON.stringify(selectedLanguages[user.login].old_value)
            }"
          >
            Apply
          </button>
        </td>
        <td>
          <button
            v-if="selectedLanguages[user.login]"
            class="btn btn-danger w-100"
            @click="deleteUser(user.login)"
          >
            X
          </button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
