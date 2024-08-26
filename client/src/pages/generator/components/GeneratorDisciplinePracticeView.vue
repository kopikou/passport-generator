<script setup lang="ts">

import {onBeforeMount, ref, watch} from "vue";
import {useQuasar} from "quasar";
import GeneratorAddPracticeDialog from "pages/generator/components/dialogs/GeneratorAddPracticeDialog.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const{
  semestersData,
}=storeToRefs(generatorViewStore)
const tab = ref(0)

function addPractice() {
  $q.dialog({
    component: GeneratorAddPracticeDialog,
    componentProps: {
      id: tab.value
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
      <span class="text-h6 q-pl-lg">Перечень практических работ по дисциплине</span>
      <p>бла бла бла</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-btn label="Добавить новую практическую рработу" color="teal" class="q-mb-md" @click="addPractice"/>
      <q-tabs
          v-model="tab"
          align="left"
          narrow-indicator
          class="q-mb-md"
      >
        <q-tab class="text-teal bg-grey-4"  v-for="item in semestersData" :name="`${item.num}`" :label="`${item.num}`"/>
      </q-tabs>
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
