<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";
const generatorViewStore = useGeneratorViewStore()

const {
  rpdData,
  indicatorsData,
  admissionData,
} = storeToRefs(generatorViewStore)

const cols = ref([
  {name: 'competence_index', field: 'competence_index', label: 'Код', align: 'left'},
  {name: 'competence', field: 'competence', label: 'Компетенция', align: 'left', },
])

const competenceList = ref([])

const filteredData = computed(() => {
  return _.orderBy(competenceList.value, x => x.competence_index)
})

watch(indicatorsData, () =>{
  competenceList.value = _.uniqBy(indicatorsData.value, (x) => x.competence_index)
}, {immediate: true})

</script>

<template>
  <div class="q-px-md">
      <span v-if="admissionData.cadmkind != 5" class="text-h6">Компетенции по дисциплине</span>
      <span v-else class="text-h6">Результаты освоения программы</span>
      <p v-if="admissionData.cadmkind != 5">В результате освоения дисциплины "{{ rpdData.planlines?.dis }}" у обучающихся должны быть сформированы компетенции. Данные
        автоматически получены из учебного плана.</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div class="q-pb-md">
        <q-table
          :columns="cols"
          :rows="filteredData"
          wrap-cells
          no-data-label="Нет данных"
          :rows-per-page-options="[]"
        >

        </q-table>
      </div>
  </div>
</template>

<style scoped>

</style>
