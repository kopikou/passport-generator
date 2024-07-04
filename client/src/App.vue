<script setup lang="ts">
import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";

const mainStore = useMainStore();
const {
  isAuthenticated,
  isStaff,
  lastName,
  firstName,
} = storeToRefs(mainStore)

</script>



<template>
  {{ firstName }}
  <router-view />
</template>
