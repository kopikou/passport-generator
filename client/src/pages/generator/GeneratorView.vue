<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, watch} from "vue";
import _ from "lodash";
import {useQuasar} from "quasar";
import {useRouter} from "vue-router";
import GeneratorLeftMenu from "pages/generator/components/GeneratorLeftMenu.vue";
import GeneratorCopyDialog from "pages/generator/components/dialogs/GeneratorCopyDialog.vue";

const generatorViewStore = useGeneratorViewStore();

const $q = useQuasar()
const router = useRouter()

const {
  cafData,
  activeRpdId,
  rpdData,
} = storeToRefs(generatorViewStore)

const props = defineProps({
    id: {
      required: true
    }
  }
)

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

function copyProgram() {
    $q.dialog({
    component: GeneratorCopyDialog,
  }).onOk((data) => {
      // console.log(data)
  })
}

watch(() => props.id,
  () => {
    activeRpdId.value = props.id
  },
  {immediate: true})

</script>

<template>
  <div class="generator-container">
    <div class="generator-container__buttons q-pa-md q-gutter-x-sm">
      <q-btn
        color="secondary"
        label="Назад к списку"
        @click="router.push('/generator/')"
      />
      <q-btn
        label="Копирование"
        color="primary"
        @click="copyProgram"
      />
    </div>
    <div class="q-pa-md generator-container__header">
      <div class="text-center">
        <div class="text-h6">
          Генератор рабочей программы дисциплины ИРНИТУ
        </div>
        <div class="text-subtitle1">
          {{ rpdData.planlines?.plan.abbrprofile }} {{
          rpdData.planlines?.plan.startyear
        }} {{ rpdData.planlines?.dis }}
        </div>
      </div>
    </div>
    <div class="generator-container__menu">
<!--      <div class="text-subtitle1 q-pl-md">{{ rpdData.planlines?.plan.abbrprofile }} {{-->
<!--          rpdData.planlines?.plan.startyear-->
<!--        }} {{ rpdData.planlines?.dis }}-->
<!--      </div>-->
      <generator-left-menu :id="props.id"/>
    </div>
    <div class="generator-container__content q-ml-md">
      <router-view/>
    </div>
  </div>
</template>

<style scoped lang="scss">

.generator-container {
  display: grid;
  grid-template-columns: 20% auto;
  grid-template-rows: auto 1fr;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  grid-template-areas:
  "a b"
  "c d";
}

.generator-container__buttons {
  grid-area: a;
}

.generator-container__header {
  grid-area: b;
}

.generator-container__menu {
  overflow-y: auto;
  grid-area: c;
}

.generator-container__content {
  overflow-y: auto;
  grid-area: d;
}

</style>
