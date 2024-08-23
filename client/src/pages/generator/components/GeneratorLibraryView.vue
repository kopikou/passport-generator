<script setup lang="ts">

import {ref} from "vue";
import {api} from "boot/axios";
import {useQuasar} from "quasar";
import {GeneratorBookData} from "src/types";

const $q = useQuasar()

const searchVal = ref('')
const bookData = ref([])

const dopBook = ref([])
const mainBook = ref<GeneratorBookData[]>([])

const columns = ref([
  {name: 'name', label: 'Название', field: 'name', align: 'center'},
])


async function searchBook() {
  if (searchVal.value.length <= 3) {
    $q.notify({
      message: "Введите больше 3-ех символов",
      color: "negative",
    })
  } else {
    $q.loading.show({message: "Поиск книг"})
    let r = await api.get('/api/generator/search-book/', {params: {val: searchVal.value}})
    bookData.value = r.data
    $q.loading.hide()
  }
}

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Учебная литература для дисциплины</span>
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
        <q-btn color="secondary" @click="searchBook" label="Поиск" />
      </div>
      <div class="row">
        <div class="col-6">
          <div class="text-h6">Основная литература</div>
          table
          <div class="text-h6">Дополнительная литература</div>
          table
        </div>
        <div class="col-6">
          <div v-for="item in bookData">
            <q-field label="Название" stack-label filled>
              <template #control>
                <div class="text-subtitle1 self-center full-width no-outline">
                  <a v-if="item.http_link" :href="`${item.http_link}`" target="_blank">{{ item.bib_disc }}</a>
                  <span v-else>{{ item.bib_disc }}</span>
                </div>
              </template>
            </q-field>
            <div class="q-gutter-x-md q-mt-md q-mb-md">
              <q-btn color="primary" label="В основную литературу"/>
              <q-btn color="secondary" label="В дополнительную литературу"/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
