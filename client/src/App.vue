<script setup lang="ts">
import useMainStore from "stores/mainStore";
import {storeToRefs} from "pinia";

const mainStore = useMainStore();
const {
  username
} = storeToRefs(mainStore)

</script>



<template>
  {{username}}
  <router-view />
</template>
