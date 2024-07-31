<script setup>
import { useRouter, useRoute } from 'vue-router'
import { toRefs, onMounted } from 'vue'
import LanguagesList from '../components/LanguagesList.vue'
import UsersList from '../components/UsersList.vue'
import ProfileForm from '../components/ProfileForm.vue'
import TranslationEditForm from '../components/TranslationEditForm.vue'

const props = defineProps({
  auth_user: Object
})
const { auth_user } = toRefs(props)

const router = useRouter()
const route = useRoute()

onMounted(() => {
  if (!auth_user.value) {
    router.push({ name: 'login' })
  }
})
</script>

<template>
  <div class="container d-flex flex-column align-items-center w-100">
    <ul class="nav nav-tabs align-self-start w-100">
      <li class="nav-item">
        <router-link class="nav-link" :class="{ active: route.name == 'home' }" to="/"
          >Profile</router-link
        >
      </li>
      <li class="nav-item">
        <router-link
          class="nav-link"
          :class="{ active: route.name == 'translation' }"
          to="/translation"
          >Translation</router-link
        >
      </li>
      <li class="nav-item" v-if="auth_user?.roles?.includes('admin')">
        <router-link class="nav-link" :class="{ active: route.name == 'languages' }" to="/languages"
          >Languages</router-link
        >
      </li>
      <li class="nav-item" v-if="auth_user?.roles?.includes('admin')">
        <router-link class="nav-link" :class="{ active: route.name == 'users' }" to="/users"
          >Users</router-link
        >
      </li>
    </ul>
    <div class="border rounded-bottom p-3 w-100 border-top-0">
      <ProfileForm v-if="route.name == 'home'" :auth_user="auth_user" />
      <TranslationEditForm v-if="route.name == 'translation'" :auth_user="auth_user" />
      <LanguagesList v-if="auth_user?.roles?.includes('admin') && route.name == 'languages'" />
      <UsersList v-if="auth_user?.roles?.includes('admin') && route.name == 'users'" />
    </div>
  </div>
</template>
