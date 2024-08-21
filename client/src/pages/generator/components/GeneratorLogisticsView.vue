<script setup lang="ts">

import {useQuasar} from "quasar";
import {ref} from "vue";
import {api} from "boot/axios";

const $q = useQuasar()
const searchVal = ref('')
const oborudData = ref([])

async function searchOborud() {
  if (searchVal.value.length <= 3) {
    $q.notify({
      message: "Введите больше 3-ех символов",
      color: "negative",
    })
  } else {
    $q.loading.show({message: "Поиск оборудования"})
    let r = await api.get('/api/generator/search-oborud/', {params: {val: searchVal.value}})
    oborudData.value = r.data
    $q.loading.hide()
  }
}
</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Перечень материально-технического обеспечения для дисциплины</span>
      <p>бла бла бла</p>
      <q-separator class="q-mt-md q-mb-md"/>

      <div class="row q-gutter-x-md q-mb-md">
        <q-input
            label="Введите текст для поиска"
            stack-label
            v-model="searchVal"
            filled
            class="col"
            :rules="[ val => val.length >= 4 || 'Введите больше 3-ех символов']"
        />
        <q-btn color="secondary" @click="searchOborud" label="Поиск"/>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
