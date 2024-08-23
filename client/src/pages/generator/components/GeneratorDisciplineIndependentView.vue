<script setup lang="ts">

import {ref} from "vue";
import {useQuasar} from "quasar";
import GeneratorAddIndependentDialog from "pages/generator/components/dialogs/GeneratorAddIndependentDialog.vue";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";

const $q = useQuasar()

const generatorViewStore = useGeneratorViewStore();

const{
  semestersData,
}=storeToRefs(generatorViewStore)

const tab = ref(0)

function addIndependent() {
  $q.dialog({
    component: GeneratorAddIndependentDialog,
    componentProps: {
      id: tab.value
    },
  })
}
</script>

<template>
  <div>
    <div style="width: 95%">
      <span class="text-h6 q-pl-lg">Перечень самостоятельных работ по дисциплине</span>
      <p>бла бла бла</p>
      <q-separator class="q-mt-md q-mb-md"/>
      <q-btn label="Добавить новую самостоятельную работу" color="teal" class="q-mb-md" @click="addIndependent"/>
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
