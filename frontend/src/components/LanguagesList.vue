<script setup>
import axios from 'axios'
import { ref, onMounted, reactive, defineModel, computed } from 'vue'
import { useStore } from 'vuex'

const store = useStore()

const api_address = import.meta.env.VITE_API_ADDRESS

const languages = defineModel('languages')
const lang_code = defineModel('lang_code')
const lang_name = defineModel('lang_name')

const lang_names = reactive({})
const searchField = defineModel('searchField')

async function loadLanguagesList() {
  await axios
    .get(api_address + '/translations/languages')
    .then((response) => {
      languages.value = response.data
      languages.value.forEach((language) => {
        lang_names[language.code] = {
          old_value: language.name,
          new_value: language.name
        }
      })
    })
    .catch((error) => {
      console.log(error.response.data.detail)
    })
}

const new_error = ref(null)

async function addNewLanguage() {
  if (!lang_code.value) {
    new_error.value = 'Please, provide a lang code.'
    return
  }

  if (!lang_name.value) {
    new_error.value = 'Please, provide a lang name.'
    return
  }

  let lang = {
    code: lang_code.value,
    name: lang_name.value
  }

  let config = {
    headers: {
      Authorization: `Bearer ${store.getters.ACCESS}`
    }
  }

  await axios
    .post(api_address + '/translations/languages/new', lang, config)
    .then(() => {
      loadLanguagesList()
      lang_code.value = ''
      lang_name.value = ''
      new_error.value = ''
    })
    .catch((error) => {
      new_error.value = error.response.data.detail
    })
}

async function updateLanguage(code) {
  const { old_value, new_value } = lang_names[code]

  if (old_value === new_value) {
    return
  }

  if (!confirm(`Are you sure that you want to change "${old_value}" to "${new_value}"?`)) {
    return
  }

  let config = {
    headers: {
      Authorization: `Bearer ${store.getters.ACCESS}`
    }
  }

  let params = {
    name: new_value
  }

  await axios
    .put(api_address + `/translations/languages/${code}/update`, params, config)
    .then(() => {
      loadLanguagesList()
    })
    .catch((error) => {
      console.log(error.response.data.detail)
    })
}

async function deleteLanguage(code) {
  if (!confirm(`Are you sure that you want to delete ${code}?`)) {
    return
  }

  let config = {
    headers: {
      Authorization: `Bearer ${store.getters.ACCESS}`
    }
  }

  await axios
    .delete(api_address + `/translations/languages/${code}/delete`, config)
    .then(() => {
      loadLanguagesList()
    })
    .catch((error) => {
      console.log(error.response.data.detail)
    })
}

function filterLanguages() {
  if (!searchField.value) {
    return languages.value
  }
  let result = languages.value.filter((language) => {
    return (
      language.code.toLowerCase().indexOf(searchField.value.toLowerCase()) != -1 ||
      language.name.toLowerCase().indexOf(searchField.value.toLowerCase()) != -1
    )
  })
  return result
}

const filtered_languages = computed(() => filterLanguages())

onMounted(() => {
  loadLanguagesList()
})
</script>

<template>
  <input
    class="form-control mb-2"
    type="text"
    placeholder="Search languages"
    v-model="searchField"
  />
  <table class="table table-light table-striped table-hover rounded">
    <thead class="table-dark">
      <tr>
        <th scope="col">Code</th>
        <th scope="col">Name</th>
        <th></th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>
          <input
            type="text"
            class="w-100 form-control"
            placeholder="Enter new language code"
            v-model="lang_code"
          />
        </td>
        <td>
          <input
            type="text"
            class="w-100 form-control"
            placeholder="Enter new language name"
            v-model="lang_name"
          />
        </td>
        <td colspan="2">
          <button class="btn btn-primary w-100" @click="addNewLanguage">+</button>
        </td>
      </tr>
      <tr>
        <td v-if="new_error" colspan="4" class="text-danger">
          {{ new_error }}
        </td>
      </tr>
      <tr v-for="(language, index) in filtered_languages" :key="index">
        <td class="text-center">{{ language.code }}</td>
        <td>
          <input
            :name="language.code"
            type="text"
            class="w-100 form-control"
            v-model="lang_names[language.code].new_value"
          />
        </td>
        <td>
          <button
            class="btn btn-primary w-100"
            :class="{
              disabled: lang_names[language.code].new_value === lang_names[language.code].old_value
            }"
            @click="updateLanguage(language.code)"
          >
            Apply
          </button>
        </td>
        <td>
          <button class="btn btn-danger w-100" @click="deleteLanguage(language.code)">X</button>
        </td>
      </tr>
    </tbody>
  </table>
</template>
