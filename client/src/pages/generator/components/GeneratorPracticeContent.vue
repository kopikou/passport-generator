<script setup lang="ts">

import {ref} from "vue";

const content = ref()

const columns = [
  {name: 'num', label: '№ п/п', field: 'num', align: 'center'},
  {name: 'part', label: 'Этап', field: 'part', align: 'center'},
  {name: 'content', label: 'Содержание работ', field: 'content', align: 'center'},
]

</script>

<template>
<div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Содержание практики</span>
      <p></p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div class="q-gutter-y-md">
        <q-input
          label="Содержание практики"
          filled
          type="textarea"
          v-model="content"
        />
        <q-table
          :colums="columns"
          :rows="[]"
          no-data-label="Не заполнено"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
