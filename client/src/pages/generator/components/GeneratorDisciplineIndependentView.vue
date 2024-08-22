<script setup lang="ts">

import {ref} from "vue";

const tab = ref(0)
</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Перечень самостоятельных работ по дисциплине</span>
      <p>бла бла бла</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-btn label="Добавить новую самостоятельную работу" color="teal" class="q-mb-md" @click="addTheme"/>
      <q-tabs
          v-model="tab"
          align="left"
          narrow-indicator
          class="q-mb-md"
      >
        <q-tab class="text-teal bg-grey-4" name="1" label="1"/>
        <q-tab class="text-teal bg-grey-4" name="2" label="2"/>
      </q-tabs>
      <q-tab-panels
          v-model="tab"
          animated
          transition-prev="scale"
          transition-next="scale"
      >
        <q-tab-panel v-for="i in 2" :name="`${i}`">
          hello world
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </div>
</template>

<style scoped>

</style>
