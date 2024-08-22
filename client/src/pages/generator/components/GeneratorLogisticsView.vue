<script setup lang="ts">

import {useQuasar} from "quasar";
import {ref} from "vue";
import {api} from "boot/axios";
import {storeToRefs} from "pinia";
import useGeneratorViewStore from "stores/generatorViewStore";
import {GeneratorOborudData} from "src/types";

const $q = useQuasar()
const searchVal = ref('')
const oborudData = ref<GeneratorOborudData[]>([])

const searchType = ref(1)
const typeOptions = [
  {label: 'По кафедре с ограничениям', value: 1, color: 'green'},
  {label: 'По кафедре', value: 2, color: 'blue'},
  {label: 'По университету', value: 3, color: 'red'},
]

const generatorViewStore = useGeneratorViewStore();

const {
  planlinesData,
} = storeToRefs(generatorViewStore)

async function searchOborud() {
  if (searchVal.value.length <= 3) {
    $q.notify({
      message: "Введите больше 3-ех символов",
      color: "negative",
    })
  } else {
    $q.loading.show({message: "Поиск оборудования"})
    let r = await api.get('/api/generator/search-oborud/', {params: {val: searchVal.value, caf: planlinesData.value.caf, type: searchType.value}})
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
      <q-option-group
          :options="typeOptions"
          type="radio"
          v-model="searchType"
          inline
      />
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
      <div class="row">
        <div class="col-5">
          <div class="text-h6">выбрано</div>
          table
        </div>
        <div class="col-7">
          <div v-for="item in oborudData">
            <q-field label="Название" stack-label filled>
              <template #control>
                <div class="text-subtitle1 self-center full-width no-outline">
                  <span>{{ item.name }} <q-chip v-if="item.inv" :label="`${item.inv}`"/> <q-chip v-if="item.caud__name" :label="`${item.caud__name}`" /></span>
                </div>
              </template>
            </q-field>
            <div class="q-gutter-x-md q-mt-md q-mb-md">
              <q-btn color="primary" label="Добавить"/>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
