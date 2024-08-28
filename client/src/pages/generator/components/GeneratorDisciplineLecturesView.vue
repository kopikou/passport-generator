<script setup lang="ts">

import {onBeforeMount, ref, watch, computed} from "vue";
import {useQuasar} from "quasar";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import GeneratorAddLecturesDialog from "pages/generator/components/dialogs/GeneratorAddLecturesDialog.vue";
import _ from "lodash";

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const {
  semestersData,
} = storeToRefs(generatorViewStore)

const tab = ref(0)

const allProcent = computed(() => {
  let hoursList = _.map(semestersData.value, (x) => x.lekc)
  return _.sum(hoursList)
})

const semesterProcent = computed(() => {
  let hoursList = _.map(_.filter(semestersData.value, (x) => x.num == tab.value), (x) => x.lekc)
  return _.sum(hoursList)
})

function addLectures() {
  $q.dialog({
    component: GeneratorAddLecturesDialog,
    componentProps: {
      sem: tab.value,
      id: null,
    },
  })
}

function updateLectures(id) {
  $q.dialog({
    component: GeneratorAddLecturesDialog,
    componentProps: {
      sem: tab.value,
      id: id,
    },
  })
}

watch(semestersData, () => {
  tab.value = `${semestersData.value[0].num}`
})

onBeforeMount(() => {
  tab.value = `${semestersData.value[0]?.num}`
})

</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Перечень лекционных работ по дисциплине</span>
      <p>бла бла бла</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-btn label="Добавить новую лекционную работу" color="teal" class="q-mb-md" @click="addLectures"/>
      <q-linear-progress class="q-mb-md" size="20px" rounded :value="0" color="teal">
        <div class="absolute-full flex flex-center">
          <q-badge color="white" text-color="black" :label="`0 / ${allProcent}`"/>
        </div>
      </q-linear-progress>
      <q-tabs
          v-model="tab"
          align="left"
          narrow-indicator
          class="q-mb-md"
      >
        <q-tab class="text-teal bg-grey-4" v-for="item in semestersData" :name="`${item.num}`" :label="`${item.num}`"/>
      </q-tabs>
      <q-linear-progress class="q-mb-md" size="20px" rounded :value="0" color="primary">
        <div class="absolute-full flex flex-center">
          <q-badge color="white" text-color="black" :label="`0 / ${semesterProcent}`"/>
        </div>
      </q-linear-progress>
      <q-tab-panels
          v-model="tab"
          animated
          transition-prev="scale"
          transition-next="scale"
      >
        <q-tab-panel v-for="item in semestersData" :name="`${item.num}`">
          hello world
        </q-tab-panel>
      </q-tab-panels>
    </div>
  </div>
</template>

<style scoped>

</style>
