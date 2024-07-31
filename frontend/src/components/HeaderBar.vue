<script setup>
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import { defineProps, toRefs } from 'vue'

const props = defineProps({
  login: String
})

const store = useStore()
const router = useRouter()

const { login } = toRefs(props)

function userLogout() {
  store.commit('LOGOUT')
  router.go()
}
</script>

<template>
  <div
    class="w-100 bg-dark text-light p-3 d-flex flex-row mb-5 align-items-center justify-content-between"
  >
    <div>
      <span class="fs-4">KnorozovAPI</span>
    </div>
    <div class="d-flex flex-row">
      <p class="me-2 fs-5 m-0">{{ login }}</p>
      <a
        href="#"
        @click="userLogout"
        class="link-info link-offset-2 link-underline-opacity-25 link-underline-opacity-75-hover"
        >X</a
      >
    </div>
  </div>
</template>

<style scoped></style>
