<script setup lang="ts">

import {onBeforeMount, ref, toRaw, watchEffect} from "vue";
import {api} from "boot/axios";
import useGeneratorViewStore from "stores/generatorViewStore";
import {storeToRefs} from "pinia";
import _ from "lodash";
import {useQuasar} from "quasar";

const generatorViewStore = useGeneratorViewStore();

const {
  activeRpdId,
  additionalInfo,
  guidelines,
  disabled,
} = storeToRefs(generatorViewStore)

const props = defineProps({
  label: {
    required: true,
  },
  type: {
    required: true,
  }
})
const $q = useQuasar()
const guidelines_text = ref<string>('')

async function saveData() {
  if (generatorViewStore.abortGetDataController)
    generatorViewStore.abortGetDataController.abort()

  _.set(guidelines.value, `[0].${props.type}`, guidelines_text.value)

  let r = await api.post(`/api/generator/${activeRpdId.value}/save-additional-info/`, {
    "type": 'guidelines',
    "value": guidelines.value
  })

  $q.notify({
    message: "Данные <span class='text-bold'>об методических указаний</span> сохранены!",
    color: "secondary",
    position: "bottom-right",
    html: true,
  })
  await generatorViewStore.getData();
  generatorViewStore.checkErrors()
}

watchEffect(() => {
  guidelines_text.value = _.get(guidelines.value, `[0].${props.type}`)
})

</script>

<template>
  <q-expansion-item
    :label=props.label
    v-bind="$attrs"
  >
    <q-card>
      <q-card-section>

        <q-input
          label="Методические указания"
          type="textarea"
          filled
          v-model="guidelines_text"
          :readonly="disabled"
          debounce="1000"
          @update:modelValue="saveData"
        />

        <!--        <q-btn-->
        <!--            class="q-mt-md"-->
        <!--            label="Сохранить"-->
        <!--            color="primary"-->
        <!--            @click="saveData"-->
        <!--            v-show="!disabled"-->
        <!--        />-->

      </q-card-section>
    </q-card>
  </q-expansion-item>
  <q-separator/>
</template>

<style scoped>

</style>
