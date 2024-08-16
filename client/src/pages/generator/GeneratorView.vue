<script setup lang="ts">

import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import {computed, watch} from "vue";
import _ from "lodash";
import {useQuasar} from "quasar";
import {useRouter} from "vue-router";
import GeneratorLeftMenu from "pages/generator/components/GeneratorLeftMenu.vue";

const generatorViewStore = useGeneratorViewStore();

const $q = useQuasar()
const router = useRouter()

const {
  cafData,
  activeRpdId,
  rpdData,
} = storeToRefs(generatorViewStore)

const props = defineProps(
  {
    id: {
      required: true
    }
  }
)

const cafDataById = computed(() => {
  return _.keyBy(cafData.value, 'value')
})

watch(() => props.id,
  () => {
    activeRpdId.value = props.id
  },
  {immediate: true})

</script>

<template>
  <div class="q-pa-lg">
    <div>
      <div class="text-h6 q-mb-md text-center">
          <span class="text-center">
            Генератор рабочей программы дисциплины ИРНИТУ
          </span>
      </div>
    </div>
    <div class="q-pa-md">
      <q-btn
        color="secondary"
        label="Назад к списку"
        @click="router.push('/generator/')"
      />
    </div>
    <div class="row">
      <div class="col-md-2">
          <generator-left-menu :id="props.id"/>
      </div>
      <div class="col-md-10">
        <router-view />
        {{ rpdData }}
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>
