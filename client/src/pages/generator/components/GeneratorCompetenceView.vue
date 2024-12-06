<script setup lang="ts">
import {computed, onBeforeMount, ref, watch} from "vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";
const generatorViewStore = useGeneratorViewStore()

const {
  indicatorsData,
} = storeToRefs(generatorViewStore)

const cols = ref([
  {name: 'competence_index', field: 'competence_index', label: 'Код', align: 'left'},
  {name: 'competence', field: 'competence', label: 'Компетенция', align: 'left'},
])

const competenceList = ref([])

watch(indicatorsData, () =>{
  competenceList.value = _.uniqBy(indicatorsData.value, (x) => x.competence_index)
}, {immediate: true})

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Компетенции по дисциплине</span>
      <p>В результате освоения дисциплины "Базы данных" у обучающихся должны быть сформированы компетенции. Данные
        автоматически получены из учебного плана.</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <div class="q-pb-md">
        <q-table
          :columns="cols"
          :rows="competenceList"
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
