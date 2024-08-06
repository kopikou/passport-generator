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

const $q = useQuasar()

const props = defineProps({
  id: {
    required: true,
  }
})

const planViewStore = usePlanViewStore()
const {
  activeFileId,
  disabled,
} = storeToRefs(planViewStore);

const link = ref('plan')

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
    let r = await api.get('/api/upload/accept-file/', {params: {id: props.id}})
      .then(() => {
        $q.notify({
          color: "primary",
          type: 'secondary',
          message: `Успешно, отправляем данные в АИС! :)`,
        })
      })
    location.href = '/'
  })
}

watch(() => props.id,
  () => {
    activeFileId.value = props.id
  },
  {immediate: true})

</script>

<template>
  <div class="plx-file-view-container" style="display: grid; grid-template-columns: auto 1fr; gap: 8px">
    <!--    <div v-show="disabled" class="text-center text-green text-h6">-->
    <!--      План отправлен в АИС, разрешен только просмотр-->
    <!--    </div>-->
    <div>
      <q-list
        bordered
      >
        <q-item
          clickable
          v-ripple
          :active="link === 'plan'"
          @click="link = 'plan'"
          active-class="my-menu-link"
        >

          <q-item-section avatar>
            <q-icon name="mdi-book-edit-outline"/>
          </q-item-section>

          <q-item-section>План</q-item-section>

        </q-item>
        <q-item
          clickable
          v-ripple
          :active="link === 'disciple'"
          @click="link = 'disciple'"
          active-class="my-menu-link"
        >

          <q-item-section avatar>
            <q-icon name="mdi-account-school"/>
          </q-item-section>

          <q-item-section>Дисциплины</q-item-section>

        </q-item>
        <q-item
          clickable
          v-ripple
          :active="link === 'documents'"
          @click="link = 'documents'"
          active-class="my-menu-link"
        >

          <q-item-section avatar>
            <q-icon name="mdi-file-document-outline"/>
          </q-item-section>

          <q-item-section>Документы</q-item-section>

        </q-item>
        <q-item
          clickable
          v-ripple
          :active="link === 'semester'"
          @click="link = 'semester'"
          active-class="my-menu-link"
        >

          <q-item-section avatar>
            <q-icon name="mdi-clock-alert-outline"/>
          </q-item-section>

          <q-item-section>Семестры</q-item-section>

        </q-item>
        <q-item
          clickable
          v-ripple
          :active="link === 'indicators'"
          @click="link = 'indicators'"
          active-class="my-menu-link"
        >

          <q-item-section avatar>
            <q-icon name="mdi-invoice-check-outline"/>
          </q-item-section>

          <q-item-section>Индикаторы</q-item-section>

        </q-item>
      </q-list>

      <q-btn
        label="Отправить план в АИС"
        @click="acceptPlan"
        :disable="disabled"
        class="q-mt-md my-menu-link"
        style="width: 100%"
      />

    </div>
    <div style="overflow: scroll">
        <plan-view v-if="link === 'plan'"/>
        <discipline-view v-if="link === 'disciple'"/>
        <documents-view v-if="link === 'documents'"/>
        <semester-view v-if="link === 'semester'"/>
        <indicators-view v-if="link === 'indicators'"/>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.my-menu-link {
  color: white;
  background: $;
}

.plx-file-view-container {
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  right: 0;
  overflow: hidden;
}
</style>
