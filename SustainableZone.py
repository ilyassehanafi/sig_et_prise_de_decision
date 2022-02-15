# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SustainableZone
                                 A QGIS plugin
 decide if a zone is sustainable
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2022-02-08
        git sha              : $Format:%H$
        copyright            : (C) 2022 by HANAFI ILYASSE ET MOUSSA AYMANE
        email                : ilyassehanafi@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from pydoc import cli
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
# Initialize Qt resources from file resources.py
from qgis._core import QgsVectorLayer, QgsProject, QgsFeature, QgsGeometry, QgsField

from .resources import *
# Import the code for the dialog
from .SustainableZone_dialog import SustainableZoneDialog
import os.path


class SustainableZone:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.ectAlltimes = []
        self.evAlltimes = []
        self.socAlltimes = []
        self.decisTime1 = []
        self.decisTime2 = []
        self.decisTime3 = []
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'SustainableZone_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&zonesustainable')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('SustainableZone', message)

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/SustainableZone/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u''),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&zonesustainable'),
                action)
            self.iface.removeToolBarIcon(action)

    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start is True:
            self.first_start = False
            self.dlg = SustainableZoneDialog()

        self.dlg.importButton.clicked.connect(lambda: self.getJsonFile())
        self.dlg.okButtonPage1.clicked.connect(lambda: self.switchPage(2))
        self.dlg.okButtonPage2.clicked.connect(lambda: self.switchPage(3))
        self.dlg.okButtonPage3.clicked.connect(lambda: self.switchPage(4))
        self.dlg.okButtonPage4.clicked.connect(lambda: self.switchPage(5))
        self.dlg.okButtonPage5.clicked.connect(lambda: self.switchPage(6))
        self.dlg.returnButtonPage2.clicked.connect(lambda: self.switchPage(1))
        self.dlg.returnButtonPage3.clicked.connect(lambda: self.switchPage(2))
        self.dlg.returnButtonPage4.clicked.connect(lambda: self.switchPage(3))

        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    def getJsonFile(self):
        file = str(QFileDialog.getOpenFileName(None, 'open logo file', '', "json (*.geojson *.json)")[0])
        if file:
            self.layer = QgsVectorLayer(file, os.path.basename(file), "ogr")
            QgsProject.instance().addMapLayer(self.layer)
            self.dlg.label_6.setText(file)


    def switchPage(self, pageNumber):
        if pageNumber == 1:
            self.dlg.stackedWidget.setCurrentWidget(self.dlg.page)
        elif pageNumber == 2:
            self.dlg.stackedWidget.setCurrentWidget(self.dlg.page_2)
        elif pageNumber == 3:
            self.dlg.stackedWidget.setCurrentWidget(self.dlg.page_3)
        elif pageNumber == 4:
            self.dlg.stackedWidget.setCurrentWidget(self.dlg.page_4)
        elif pageNumber == 5:
            self.dlg.stackedWidget.setCurrentWidget(self.dlg.page_5)
            self.getMatrixValues()
            a = self.getEcoEditLineTime1()
            b = self.getEcoEditLineTime2()
            c = self.getEcoEditLineTime3()
            d = self.getEnviEditLineTime1()
            e = self.getEnviEditLineTime2()
            f = self.getEnviEditLineTime3()
            g = self.getSocEditLineTime1()
            h = self.getSocEditLineTime2()
            i = self.getSocEditLineTime3()
            self.checkDurableOrNot(a, b, c, d, e, f, g, h, i)
            resultList = ["Résultat Economique", "Résultat Environmentale", "Résultat Societale"]
            self.createLayer(self.layer.clone(), resultList, "Décision time1")
            self.createLayer(self.layer.clone(), resultList, "Décision time2")
            self.createLayer(self.layer.clone(), resultList, "Décision time3")
            self.dlg.label_71.setText(str(self.ectAlltimes[0]))
            self.dlg.label_72.setText(str(self.ectAlltimes[1]))
            self.dlg.label_73.setText(str(self.ectAlltimes[2]))
            self.dlg.label_80.setText(str(self.evAlltimes[0]))
            self.dlg.label_82.setText(str(self.evAlltimes[1]))
            self.dlg.label_84.setText(str(self.evAlltimes[2]))
            self.dlg.label_92.setText(str(self.socAlltimes[0]))
            self.dlg.label_94.setText(str(self.socAlltimes[1]))
            self.dlg.label_96.setText(str(self.socAlltimes[2]))


        else:
            self.clearALL()
            self.dlg.stackedWidget.setCurrentWidget(self.dlg.page)
            self.dlg.close()


    # Calcule de l'indice economique :
    def calculEconomicIndice(self, param1, param2, param3, param4):
        infrastructure = (param1 / 400) * self.facteurEco
        ChiffreAffaire = (param2 / 500) * self.facteurEco
        nombreTouriste = (param3 / 1000) * self.facteurEco
        produitsTerroir = (param4 / 700) * self.facteurEco
        ect1 = infrastructure + ChiffreAffaire + nombreTouriste + produitsTerroir
        self.ectAlltimes.append(round(ect1/4, 2))
        return ect1 / 4

    # Calcule de l'indice Environmentale  :
    def calculEnvironmentaleIndice(self, param1, param2, param3, param4):
        biodiversite = (param1 / 900) * self.facteurEnvi
        ressourcesNaturelles = (param2 / 600) * self.facteurEnvi
        paysage = (param3 / 700) * self.facteurEnvi
        climat = (param4 / 40) * self.facteurEnvi
        ev1 = biodiversite + ressourcesNaturelles + paysage + climat
        self.evAlltimes.append(round(ev1/4, 2))
        return ev1 / 4

    # Calcule de l'indice Environmentale  :
    def calculSocietaleIndice(self, param1, param2, param3, param4):
        securite = (param1 / 68) * self.facteurSoc
        traditions = (param2 / 60) * self.facteurSoc
        Hospitalite = (param3 / 50) * self.facteurSoc
        chomage = (param4 / 50) * self.facteurSoc
        es1 = securite + traditions + Hospitalite + chomage
        self.socAlltimes.append(round(es1/4, 2))
        return es1 / 4

    def getMatrixValues(self):
        m11 = float(self.dlg.ligne11.text())
        m12 = float(self.dlg.ligne12.text())
        m13 = float(self.dlg.ligne13.text())
        m21 = float(self.dlg.ligne21.text())
        m22 = float(self.dlg.ligne22.text())
        m23 = float(self.dlg.ligne23.text())
        m31 = float(self.dlg.ligne31.text())
        m32 = float(self.dlg.ligne32.text())
        m33 = float(self.dlg.ligne33.text())
        # somme des colonnes
        sum_c1 = m11 + m21 + m31
        sum_c2 = m12 + m22 + m32
        sum_c3 = m13 + m23 + m33
        # matrice normalisee
        m11 = m11 / sum_c1
        m21 = m21 / sum_c1
        m31 = m31 / sum_c1

        m12 = m12 / sum_c2
        m22 = m22 / sum_c2
        m32 = m32 / sum_c2

        m13 = m13 / sum_c3
        m23 = m23 / sum_c3
        m33 = m33 / sum_c3
        # somme ligne

        sum_l1 = m11 + m12 + m13
        sum_l2 = m21 + m22 + m23
        sum_l3 = m31 + m32 + m33

        # new matrice
        m11 = m11 * sum_l1
        m12 = m12 * sum_l2
        m13 = m13 * sum_l3

        m21 = m21 * sum_l1
        m22 = m22 * sum_l2
        m23 = m23 * sum_l3

        m31 = m31 * sum_l1
        m32 = m32 * sum_l2
        m33 = m33 * sum_l3

        # facteur
        self.facteurEco = m11 + m12 + m13
        self.facteurEnvi = m21 + m22 + m23
        self.facteurSoc = m31 + m32 + m33
        print("facteur impact Eco")
        print(self.facteurEco)
        print("facteur impact envi")
        print(self.facteurEnvi)
        print("facteur impact Soc")
        print(self.facteurSoc)

    def getEcoEditLineTime1(self):
        # Economique
        p1Time1Eco = float(self.dlg.p1Time1Eco.text())
        p2Time1Eco = float(self.dlg.p2Time1Eco.text())
        p3Time1Eco = float(self.dlg.p3Time1Eco.text())
        p4Time1Eco = float(self.dlg.p4Time1Eco.text())
        return self.calculEconomicIndice(p1Time1Eco, p2Time1Eco, p3Time1Eco, p4Time1Eco)

    def getEnviEditLineTime1(self):
        # Environement
        p1Time1Envi = float(self.dlg.p1Time1Envi.text())
        p2Time1Envi = float(self.dlg.p2Time1Envi.text())
        p3Time1Envi = float(self.dlg.p3Time1Envi.text())
        p4Time1Envi = float(self.dlg.p4Time1Envi.text())
        return self.calculEnvironmentaleIndice(p1Time1Envi, p2Time1Envi, p3Time1Envi, p4Time1Envi)

    def getSocEditLineTime1(self):
        # Societe
        p1Time1Soc = float(self.dlg.p1Time1Soc.text())
        p2Time1Soc = float(self.dlg.p2Time1Soc.text())
        p3Time1Soc = float(self.dlg.p3Time1Soc.text())
        p4Time1Soc = float(self.dlg.p4Time1Soc.text())
        return self.calculSocietaleIndice(p1Time1Soc, p2Time1Soc, p3Time1Soc, p4Time1Soc)

    def getEcoEditLineTime2(self):
        # Economique
        p1Time2Eco = float(self.dlg.p1Time2Eco.text())
        p2Time2Eco = float(self.dlg.p2Time2Eco.text())
        p3Time2Eco = float(self.dlg.p3Time2Eco.text())
        p4Time2Eco = float(self.dlg.p4Time2Eco.text())
        return self.calculEconomicIndice(p1Time2Eco, p2Time2Eco, p3Time2Eco, p4Time2Eco)

    def getEnviEditLineTime2(self):
        # Environement
        p1Time2Envi = float(self.dlg.p1Time2Envi.text())
        p2Time2Envi = float(self.dlg.p2Time2Envi.text())
        p3Time2Envi = float(self.dlg.p3Time2Envi.text())
        p4Time2Envi = float(self.dlg.p4Time2Envi.text())
        return self.calculEnvironmentaleIndice(p1Time2Envi, p2Time2Envi, p3Time2Envi, p4Time2Envi)

    def getSocEditLineTime2(self):
        # Societe
        p1Time2Soc = float(self.dlg.p1Time2Soc.text())
        p2Time2Soc = float(self.dlg.p2Time2Soc.text())
        p3Time2Soc = float(self.dlg.p3Time2Soc.text())
        p4Time2Soc = float(self.dlg.p4Time2Soc.text())
        return self.calculSocietaleIndice(p1Time2Soc, p2Time2Soc, p3Time2Soc, p4Time2Soc)

    def getEcoEditLineTime3(self):
        # Economique
        p1Time3Eco = float(self.dlg.p1Time3Eco.text())
        p2Time3Eco = float(self.dlg.p2Time3Eco.text())
        p3Time3Eco = float(self.dlg.p3Time3Eco.text())
        p4Time3Eco = float(self.dlg.p4Time3Eco.text())
        return self.calculEconomicIndice(p1Time3Eco, p2Time3Eco, p3Time3Eco, p4Time3Eco)

    def getEnviEditLineTime3(self):
        # Environement
        p1Time3Envi = float(self.dlg.p1Time3Envi.text())
        p2Time3Envi = float(self.dlg.p2Time3Envi.text())
        p3Time3Envi = float(self.dlg.p3Time3Envi.text())
        p4Time3Envi = float(self.dlg.p4Time3Envi.text())
        return self.calculEnvironmentaleIndice(p1Time3Envi, p2Time3Envi, p3Time3Envi, p4Time3Envi)

    def getSocEditLineTime3(self):
        # Societe
        p1Time3Soc = float(self.dlg.p1Time3Soc.text())
        p2Time3Soc = float(self.dlg.p2Time3Soc.text())
        p3Time3Soc = float(self.dlg.p3Time3Soc.text())
        p4Time3Soc = float(self.dlg.p4Time3Soc.text())
        return self.calculSocietaleIndice(p1Time3Soc, p2Time3Soc, p3Time3Soc, p4Time3Soc)

    def checkDurableOrNot(self, a, b, c, d, e, f, g, h, i):
        seuil_eco = float(self.dlg.seuilEco.text())
        seuil_envi = float(self.dlg.seuilEnvi.text())
        seuil_soc = float(self.dlg.seuilSoc.text())

        if a < (seuil_eco * 4):
            self.dlg.ecoDecisTime1.setText("Non durable")
            self.decisTime1.append("Non durable")
        else:
            self.dlg.ecoDecisTime1.setText("durable")
            self.decisTime1.append("durable")

        if b < (seuil_eco * 4):
            self.dlg.ecoDecisTime2.setText("Non durable")
            self.decisTime2.append("Non durable")
        else:
            self.dlg.ecoDecisTime2.setText("durable")
            self.decisTime2.append("durable")

        if c < (seuil_eco * 4):
            self.dlg.ecoDecisTime3.setText("Non durable")
            self.decisTime3.append("Non durable")
        else:
            self.dlg.ecoDecisTime3.setText("durable")
            self.decisTime3.append("durable")

        if d < (seuil_envi * 4):
            self.dlg.enviDecisTime1.setText("Non durable")
            self.decisTime1.append("Non durable")
        else:
            self.dlg.enviDecisTime1.setText("durable")
            self.decisTime1.append("durable")

        if e < (seuil_envi * 4):
            self.dlg.enviDecisTime2.setText("Non durable")
            self.decisTime2.append("Non durable")
        else:
            self.dlg.enviDecisTime2.setText("durable")
            self.decisTime2.append("durable")

        if f < (seuil_envi * 4):
            self.dlg.enviDecisTime3.setText("Non durable")
            self.decisTime3.append("Non durable")
        else:
            self.dlg.enviDecisTime3.setText("durable")
            self.decisTime3.append("durable")

        if g < (seuil_soc * 4):
            self.dlg.socDecisTime1.setText("Non durable")
            self.decisTime1.append("Non durable")
        else:
            self.dlg.socDecisTime1.setText("durable")
            self.decisTime1.append("durable")
        if h < (seuil_soc * 4):
            self.dlg.socDecisTime2.setText("Non durable")
            self.decisTime2.append("Non durable")
        else:
            self.dlg.socDecisTime2.setText("durable")
            self.decisTime2.append("durable")
        if i < (seuil_soc * 4):
            self.dlg.socDecisTime3.setText("Non durable")
            self.decisTime3.append("Non durable")
        else:
            self.dlg.socDecisTime3.setText("durable")
            self.decisTime3.append("durable")

    def createLayer(self, layer, string, layerName):
        feats = [feat for feat in layer.getFeatures()]

        newLayer = QgsVectorLayer("Polygon", layerName, "memory")

        mem_layer_data = newLayer.dataProvider()
        attr = layer.dataProvider().fields().toList()
        mem_layer_data.addAttributes(attr)
        newLayer.updateFields()
        mem_layer_data.addFeatures(feats)

        pr = newLayer.dataProvider()  # need to create a data provider
        i = 0
        for i in range(3):
            pr.addAttributes([QgsField(string[i], QVariant.String)])  # define/add field data type
        feature = QgsFeature()

        li = [None] * len(attr)
        if layerName == "Décision time1":
            for decis in self.decisTime1:
                li.append(decis)
        elif layerName == "Décision time2":
            for decis in self.decisTime2:
                li.append(decis)
        else:
            for decis in self.decisTime3:
                li.append(decis)

        feature.setAttributes(li)
        newLayer.updateFields()
        pr.addFeatures([feature])
        # mem_layer_data.addFeatures(feature)
        QgsProject.instance().addMapLayer(newLayer)

    def clearALL(self):
        self.decisTime1.clear()
        self.decisTime2.clear()
        self.decisTime3.clear()
