<script setup>
import axios from 'axios'
import { defineModel, onMounted, defineProps, reactive, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

defineProps({
  auth_user: String
})

const api_address = import.meta.env.VITE_API_ADDRESS
const store = useStore()
const router = useRouter()

const translation = reactive([])
const new_entries = reactive({})
const old_translation = ref([])
const languages = ref([])

const new_page_name = defineModel('new_page_name')

async function getTranslation() {
  return await axios
    .get(api_address + '/translations/pages')
    .then((response) => {
      translation.value = []
      old_translation.value = []
      let i = 0
      old_translation.value = JSON.parse(JSON.stringify(response.data))
      response.data.forEach((page) => {
        new_entries[page.name] = ''
        translation[i] = page
        i += 1
      })
    })
    .catch((error) => console.log(error))
}

async function setTranslation(page_name, entry_key, lang, value) {
  if (!confirm(`Are you sure that you want to change "${entry_key}"?`)) {
    return
  }

  let config = {
    headers: {
      Authorization: `Bearer ${store.getters.ACCESS}`
    }
  }

  let params = {
    text: value
  }

  await axios
    .put(api_address + `/translations/pages/${page_name}/${entry_key}/${lang}/set`, params, config)
    .then(() => {
      loadData()
    })
    .catch((error) => {
      console.log(error)
    })
}

async function addPage() {
  let config = {
    headers: {
      Authorization: `Bearer ${store.getters.ACCESS}`
    }
  }

  let params = {
    name: new_page_name.value,
    entries: []
  }

  await axios
    .post(api_address + '/translations/pages/new', params, config)
    .then(() => {
      loadData()
      router.go()
    })
    .catch((error) => {
      console.log(error)
    })
}

async function addEntry(page_name) {
  let config = {
    headers: {
      Authorization: `Bearer ${store.getters.ACCESS}`
    }
  }

  let params = {
    key: new_entries[page_name]
  }

  await axios
    .post(api_address + `/translations/pages/${page_name}/new_entry`, params, config)
    .then(() => {
      loadData()
      router.go()
    })
    .catch((error) => {
      console.log(error)
    })
}

async function deletePage(page_name) {
  if (!confirm(`Are you sure that you want to delete "${page_name}"?`)) {
    return
  }

  let config = {
    headers: {
      Authorization: `Bearer ${store.getters.ACCESS}`
    }
  }

  await axios
    .delete(api_address + `/translations/pages/${page_name}/delete`, config)
    .then(() => {
      loadData()
      router.go()
    })
    .catch((error) => {
      console.log(error)
    })
}

async function deleteEntry(page_name, entry_key) {
  if (!confirm(`Are you sure that you want to delete "${entry_key}"?`)) {
    return
  }

  let config = {
    headers: {
      Authorization: `Bearer ${store.getters.ACCESS}`
    }
  }

  await axios
    .delete(api_address + `/translations/pages/${page_name}/${entry_key}/delete`, config)
    .then(() => {
      loadData()
      router.go()
    })
    .catch((error) => {
      console.log(error)
    })
}

async function loadLanguages() {
  await axios
    .get(api_address + '/translations/languages')
    .then((response) => {
      languages.value = []
      response.data.forEach((language) => {
        languages.value.push(language.code)
      })
    })
    .catch((error) => {
      console.log(error)
    })
}

function downloadTranslation() {
  const element = document.createElement('a')
  element.setAttribute(
    'href',
    'data:application/json;charset=utf-8,' +
      encodeURIComponent(JSON.stringify(translation, null, 4))
  )
  element.setAttribute('download', 'translation')
  element.style.display = 'none'
  document.body.appendChild(element)
  element.click()
  document.body.removeChild(element)
}

async function loadData() {
  new_page_name.value = ''
  await loadLanguages()
  await getTranslation()
}

onMounted(() => {
  loadData()
})
</script>

<template>
  <div class="d-flex flex-row w-100 input-group mb-2" v-if="auth_user?.roles.includes('admin')">
    <input
      type="text"
      class="form-control"
      placeholder="Enter new page name"
      v-model="new_page_name"
    />
    <button class="btn btn-primary" :class="{ disabled: new_page_name === '' }" @click="addPage()">
      +
    </button>
  </div>
  <div class="accordion" id="accordionTranslation">
    <div class="accordion-item" v-for="(page, t_index) in translation" :key="t_index">
      <h2 class="accordion-header">
        <button
          class="accordion-button"
          type="button"
          data-bs-toggle="collapse"
          :data-bs-target="`#collapse_${page.name}`"
          aria-expanded="true"
          aria-controls="collapseOne"
        >
          {{ page.name }}
        </button>
      </h2>
      <div
        :id="`collapse_${page.name}`"
        class="accordion-collapse collapse"
        data-bs-parent="#accordionTranslation"
      >
        <div class="accordion-body">
          <div
            class="d-flex flex-row w-100 input-group mb-2"
            v-if="auth_user.roles.includes('admin')"
          >
            <input
              type="text"
              class="form-control"
              placeholder="Enter new entry name"
              v-model="new_entries[page.name]"
            />
            <button
              class="btn btn-primary"
              :class="{ disabled: new_entries[page.name] === '' }"
              @click="addEntry(page.name)"
            >
              +
            </button>
          </div>
          <div v-for="(entry, e_index) in page.entries" :key="e_index">
            <caption class="fs-4 underline">
              {{
                entry.key
              }}
            </caption>
            <table class="table table-light table-striped table-hover rounded">
              <thead>
                <tr>
                  <th scope="col">language</th>
                  <th scope="col">value</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                <template v-for="(lang, l_index) in languages" :key="l_index">
                  <tr v-if="auth_user.roles.includes('admin') || auth_user.roles.includes(lang)">
                    <td>{{ lang }}</td>
                    <td>
                      <input
                        :name="`${entry.key}-${lang}`"
                        type="text"
                        class="w-100 form-control"
                        v-model="translation[t_index].entries[e_index].translations[lang]"
                      />
                    </td>
                    <td>
                      <button
                        class="btn btn-primary w-100"
                        @click="
                          setTranslation(
                            page.name,
                            entry.key,
                            lang,
                            translation[t_index].entries[e_index].translations[lang]
                          )
                        "
                        :class="{
                          disabled:
                            translation[t_index].entries[e_index].translations[lang] ===
                            old_translation[t_index].entries[e_index].translations[lang]
                        }"
                      >
                        Apply
                      </button>
                    </td>
                  </tr>
                </template>
              </tbody>
            </table>
            <button
              v-if="auth_user.roles.includes('admin')"
              class="btn btn-sm btn-danger w-100 mb-5"
              @click="deleteEntry(page.name, entry.key)"
            >
              Delete entry
            </button>
          </div>
          <hr v-if="auth_user.roles.includes('admin')" />
          <button
            v-if="auth_user.roles.includes('admin')"
            class="btn btn-danger w-100"
            @click="deletePage(page.name)"
          >
            Delete page
          </button>
        </div>
      </div>
    </div>
  </div>
  <button class="btn btn-primary w-100 mt-2" @click="downloadTranslation()">
    Download translation
  </button>
</template>
