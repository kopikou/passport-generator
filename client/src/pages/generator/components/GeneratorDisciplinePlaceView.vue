<script setup lang="ts">

import {ref} from "vue";
import {bi0CircleFill} from "@quasar/extras/bootstrap-icons";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";

const generatorViewStore = useGeneratorViewStore();

const {
  otherDiscipline,
} = storeToRefs(generatorViewStore)

const precedence = ref([])
const subsequent = ref([])

const listDiscipline = ref(otherDiscipline)
const filteredDiscipline = ref(listDiscipline.value)

function filterDiscipline(val, update) {
  update(() => {
    if (val === '') {
      filteredDiscipline.value = listDiscipline.value
    } else {
      const needle = val.toLowerCase()
      filteredDiscipline.value = _.filter(listDiscipline.value, (x) => {
        return x.dis.toLowerCase().indexOf(needle) > -1
      })
    }
  })
}

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Место дисциплины "Базы данных" в структуре ООП</span>
      <p>бла бла бла</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-select
        label="Обеспечивающие (предшествующие) дисциплины и практики"
        stack-label
        filled
        use-chips
        clearable
        use-input
        multiple
        option-label="dis"
        option-value="disid"
        :options="listDiscipline"
        v-model="precedence"
        @filter="filterDiscipline"
      />
      <br/>
      <q-select
        label="Обеспечиваемые (последующие) дисциплины и практики"
        stack-label
        filled
        use-chips
        clearable
        use-input
        multiple
        emit-value
        map-options
        option-label="dis"
        option-value="disid"
        :options="listDiscipline"
        v-model="subsequent"
        @filter="filterDiscipline"
      />
    </div>
  </div>
</template>

<style scoped>

</style>
