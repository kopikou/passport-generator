<script setup lang="ts">

import {computed, onBeforeMount, ref, watch} from "vue";
import PlanView from "pages/plx/components/PlxPlanView.vue";
import DisciplineView from "pages/plx/components/PlxDisciplineView.vue";
import DocumentsView from "pages/plx/components/PlxDocumentsView.vue";
import CompetencesView from "components/CompetencesView.vue";
import IndicatorsView from "pages/plx/components/PlxIndicatorsView.vue";
import SemesterView from "pages/plx/components/PlxSemesterView.vue";
import {useQuasar} from "quasar";
import _ from "lodash";
import {api} from "boot/axios";
import usePlanViewStore from "stores/planViewStore";
import {storeToRefs} from "pinia";
import {useRouter} from "vue-router";

const $q = useQuasar()
const router = useRouter()

const props = defineProps({
  id: {
    required: true,
  }
})

const planViewStore = usePlanViewStore()
const {
  activeFileId,
  activeFile,
  disabled,
  fileData,
  files,
} = storeToRefs(planViewStore);


function acceptPlan() {
  $q.dialog({
    title: 'Предупреждение',
    message: "<p style='font-size: 16px'>Вы уверены, что хотите синхронизировать план? <br/> В дальнейшем план нельзя будет изменить <br/> <span class='text-red-9'>Для продолжения введите \"Подтвердить\"</span></p>",
    cancel: {
      label: 'Отмена',
      flat: true,
    },
    ok: {
      label: 'Подтвердить',
      flat: true,
    },
    html: true,
    prompt: {
      model: '',
      isValid: val => val.toLowerCase() == 'подтвердить',
      type: "text",
    }
  }).onOk(async () => {
    let r = await api.get('/api/plx/accept-file/', {params: {id: props.id}})

    $q.notify({
      color: "primary",
      type: 'secondary',
      message: `Успешно, отправляем данные в АИС! :)`,
    })

    await router.push('/')
  })
}

watch(() => props.id,
  () => {
    activeFileId.value = props.id
  },
  {immediate: true})

</script>

<template>
  <div class="plx-file-view-container" style="display: grid; grid-template-columns: auto 1fr; gap: 2px">
    <!--    <div v-show="disabled" class="text-center text-green text-h6">-->
    <!--      План отправлен в АИС, разрешен только просмотр-->
    <!--    </div>-->
    <div class="q-py-sm q-pl-sm">
      <q-select filled :options="files" option-label="title" v-model="activeFile" map-options emit-value></q-select>

      <q-list
        bordered
        separator
      >
        <q-item
          clickable
          v-ripple
          active-class="bg-amber-4 text-black"
          :to="`/plx/${id}/disciplines`"
        >
          <q-item-section avatar>
            <q-icon name="mdi-account-school"/>
          </q-item-section>

          <q-item-section>Дисциплины</q-item-section>

        </q-item>
        <q-item
          clickable
          v-ripple
          active-class="bg-amber-4 text-black"
          :to="`/plx/${id}/documents`"
        >

          <q-item-section avatar>
            <q-icon name="mdi-file-document-outline"/>
          </q-item-section>

          <q-item-section>Документы</q-item-section>

        </q-item>
        <q-item
          clickable
          v-ripple
          active-class="bg-amber-4 text-black"
          :to="`/plx/${id}/semesters`"
        >

          <q-item-section avatar>
            <q-icon name="mdi-clock-alert-outline"/>
          </q-item-section>

          <q-item-section>Семестры</q-item-section>

        </q-item>
        <q-item
          clickable
          v-ripple
          active-class="bg-amber-4 text-black"
          :to="`/plx/${id}/indicators`"
        >

          <q-item-section avatar>
            <q-icon name="mdi-invoice-check-outline"/>
          </q-item-section>

          <q-item-section>Индикаторы</q-item-section>

        </q-item>
      </q-list>

      <div class="q-mt-xs">
        <template v-if="!disabled">
          <q-btn
            label="Отправить план в АИС"
            @click="acceptPlan"
            :disable="disabled"
            color="blue-10"

          />
        </template>
        <template v-else>
          <q-chip square color="green-2">
            <q-avatar icon="bookmark" color="green" text-color="white" />
            {{ fileData.status_verbose }}
          </q-chip>
        </template>
      </div>

    </div>
    <div style="display: grid; grid-template-rows: auto 1fr; overflow: hidden">
      <div class="q-ma-sm">
        <plan-view/>
      </div>
      <div style="overflow: hidden" class="q-ml-sm">
        <router-view/>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.plx-file-link__active {
  color: white;
  background: $purple-3;
}

.plx-file-view-container {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  overflow: hidden;
}

:deep(.q-table__container) {
  overflow: hidden;
  max-height: 100%
}

:deep(table thead tr th) {
  position: sticky;
  top: 0;
  background-color: white;
  z-index: 1;
}

</style>
