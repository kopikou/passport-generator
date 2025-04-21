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
  planlinesData,
} = storeToRefs(generatorViewStore)

const cols = ref([
  {name: 'competence_index', field: 'competence_index', label: 'Код', align: 'left'},
  {name: 'competence', field: 'competence', label: 'Компетенция', align: 'left'},
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
  <div>
    <div style="width: 95%">
      <div v-if="!planlinesData.viewpract">
        <span v-if="admissionData.cadmkind != 5" class="text-h6 q-pl-lg">Компетенции по дисциплине</span>
        <span v-else class="text-h6 q-pl-lg">Результаты освоения программы</span>
      </div>
      <div v-else>
        <span class="text-h6 q-pl-lg" v-if="admissionData.cadmkind != 5">Компетенции по практике</span>
        <span class="text-h6 q-pl-lg" v-else>Результаты освоения практики</span>
      </div>
      <p v-if="admissionData.cadmkind != 5">В результате освоения
        <span v-if="planlinesData.viewpract">практики</span>
        <span v-else>дисциплины</span>
        "{{ rpdData.planlines?.dis }}" у обучающихся должны быть сформированы компетенции. Данные
        автоматически получены из учебного плана.</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div class="q-pb-md">
        <q-table
          :columns="cols"
          :rows="filteredData"
          no-data-label="Нет данных"
          :rows-per-page-options="[]"
        >

        </q-table>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
