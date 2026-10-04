// Usage: swift render.swift <input.html> <output.png> <width>
import AppKit
import WebKit

let args = CommandLine.arguments
let input = URL(fileURLWithPath: args[1])
let output = URL(fileURLWithPath: args[2])
let width = CGFloat(Double(args[3]) ?? 1440)

class Renderer: NSObject, WKNavigationDelegate {
    let web: WKWebView
    init(width: CGFloat) {
        web = WKWebView(frame: NSRect(x: 0, y: 0, width: width, height: 1000))
        super.init()
        web.navigationDelegate = self
    }
    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.6) {
            webView.evaluateJavaScript("Math.ceil(document.documentElement.scrollHeight)") { result, _ in
                let h = CGFloat((result as? NSNumber)?.doubleValue ?? 1000)
                webView.frame = NSRect(x: 0, y: 0, width: width, height: h)
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.6) {
                    let cfg = WKSnapshotConfiguration()
                    cfg.rect = NSRect(x: 0, y: 0, width: width, height: h)
                    cfg.snapshotWidth = NSNumber(value: Double(width))
                    webView.takeSnapshot(with: cfg) { image, error in
                        guard let image = image,
                              let tiff = image.tiffRepresentation,
                              let rep = NSBitmapImageRep(data: tiff),
                              let png = rep.representation(using: .png, properties: [:]) else {
                            print("snapshot failed: \(String(describing: error))"); exit(1)
                        }
                        try! png.write(to: output)
                        print("wrote \(output.path) \(Int(width))x\(Int(h))")
                        exit(0)
                    }
                }
            }
        }
    }
}

let app = NSApplication.shared
app.setActivationPolicy(.prohibited)
let r = Renderer(width: width)
r.web.loadFileURL(input, allowingReadAccessTo: input.deletingLastPathComponent())
DispatchQueue.main.asyncAfter(deadline: .now() + 30) { print("timeout"); exit(2) }
app.run()
