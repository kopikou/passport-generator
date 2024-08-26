<script setup lang="ts">

import {onBeforeMount, ref, watch} from "vue";
import {bi0CircleFill} from "@quasar/extras/bootstrap-icons";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";
import QSelectFilterable from "components/QSelectFilterable.vue";
import {api} from "boot/axios";

const generatorViewStore = useGeneratorViewStore();

const {
  otherDiscipline,
  activeRpdId,
  rpdData,
} = storeToRefs(generatorViewStore)

const precedence = ref(rpdData.value.precedence_discipline)
const subsequent = ref(rpdData.value.subsequent_discipline)

const listDiscipline = ref(otherDiscipline)
const filteredDiscipline = ref(listDiscipline.value)

async function savePrecSubDiscipline() {
  let r = await api.post(`/api/generator/${activeRpdId.value}/save-prec-sub-discipline/`, {
    id: activeRpdId.value,
    precedence_discipline: precedence.value,
    subsequent_discipline: subsequent.value,
  })

  rpdData.value.subsequent_discipline = r.data.subsequent_discipline
  rpdData.value.precedence_discipline = r.data.precedence_discipline
}

watch(rpdData, () => {
  precedence.value = rpdData.value.precedence_discipline
  subsequent.value = rpdData.value.subsequent_discipline
})

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Место дисциплины в структуре ООП</span>
      <p>бла бла бла</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-select-filterable
        label="Обеспечивающие (предшествующие) дисциплины и практики"
        v-model="precedence"
        option-label="dis"
        option-value="disid"
        stack-label
        filled
        use-chips
        clearable
        multiple
        map-options
        emit-value
        :options="otherDiscipline"
      />
      <br/>
      <q-select-filterable
        label="Обеспечиваемые (последующие) дисциплины и практики"
        v-model="subsequent"
        option-label="dis"
        option-value="disid"
        stack-label
        filled
        use-chips
        clearable
        multiple
        map-options
        emit-value
        :options="otherDiscipline"
      />
      <q-btn label="Сохранить" color="primary" class="q-mt-sm" @click="savePrecSubDiscipline"/>
    </div>
  </div>
</template>

<style scoped>

</style>
