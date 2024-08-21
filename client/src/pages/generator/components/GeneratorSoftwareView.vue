<script setup lang="ts">

import {useQuasar} from "quasar";
import {api} from "boot/axios";
import {ref} from "vue";
import {SoftwareData} from "src/types";

const $q = useQuasar()
const searchVal = ref('')
const softwareData = ref<SoftwareData[]>([])

async function searchSoft() {
  if (searchVal.value.length <= 3) {
    $q.notify({
      message: "Введите больше 3-ех символов",
      color: "negative",
    })
  } else {
    $q.loading.show({message: "Поиск программного обеспечения"})
    let r = await api.get('/api/generator/search-software/', {params: {val: searchVal.value}})
    softwareData.value = r.data
    $q.loading.hide()
  }
}
</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Перечень лицензионного программного обеспечения для дисциплины</span>
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
        <q-btn color="secondary" @click="searchSoft" label="Поиск"/>
      </div>
            <div class="row">
        <div class="col-5">
          <div class="text-h6">выбрано</div>
          table
        </div>
        <div class="col-7">
          <div v-for="item in softwareData">
            <q-field label="Название" stack-label filled>
              <template #control>
                <div class="text-subtitle1 self-center full-width no-outline">
                  <span>{{ item.clicense__name }}</span>
                </div>
              </template>
            </q-field>
            <div class="q-gutter-x-md q-mt-md q-mb-md">
              <q-btn color="primary" label="Добавить"/>
            </div>
          </div>
        </div>
      </div>
      {{ softwareData }}
    </div>
  </div>
</template>

<style scoped>

</style>
